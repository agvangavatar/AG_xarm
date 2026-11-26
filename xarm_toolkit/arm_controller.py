# src/xarm_toolkit/arm_controller.py
"""Serial control of the Hiwonder xArm via its controller-board (LSC) protocol."""
""" This file used Gemini Notebook LLM and Claude as a guide """


import logging
import struct

import serial

logger = logging.getLogger(__name__)

MIN_POSITION, MAX_POSITION = 0, 1000
MIN_SERVO_ID, MAX_SERVO_ID = 1, 6
MAX_DURATION_MS = 0xFFFF


class ArmController:
    """Owns the serial link and exposes intention-revealing arm operations."""

    def __init__(self, port: str, baud: int = 9600, timeout: float = 0.5) -> None:
        self._serial = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    @staticmethod
    def build_frame(command: int, params: bytes = b"") -> bytes:
        """Assemble ``55 55 / Length / Command / Params`` (Length = len(params) + 2)."""
        if not 0 <= command <= 0xFF:
            raise ValueError(f"Command out of range: {command}")
        length = len(params) + 2
        if length > 0xFF:
            raise ValueError("Parameters too long for one frame")
        return bytes([0x55, 0x55, length, command]) + bytes(params)

    def _write(self, frame: bytes) -> None:
        """Send one frame down the wire and log it."""
        logger.debug("TX: %s", frame.hex(" "))
        self._serial.write(frame)

    def move_servos(self, moves, duration_ms: int) -> None:
        """Move several servos together in one CMD_SERVO_MOVE (0x03) frame."""
        moves = list(moves)
        if not moves:
            raise ValueError("No servo moves given")
        if len(moves) > 0xFF:
            raise ValueError("Too many servos in one move")
        if not 0 <= duration_ms <= MAX_DURATION_MS:
            raise ValueError(f"duration_ms out of range: {duration_ms}")
        for servo_id, position in moves:
            if not MIN_SERVO_ID <= servo_id <= MAX_SERVO_ID:
                raise ValueError(f"servo_id out of range: {servo_id}")
            if not MIN_POSITION <= position <= MAX_POSITION:
                raise ValueError(f"position out of range: {position}")

        params = struct.pack("<BH", len(moves), duration_ms)
        for servo_id, position in moves:
            params += struct.pack("<BH", servo_id, position)
        self._write(self.build_frame(0x03, params))

    def move_servo(self, servo_id: int, position: int, duration_ms: int) -> None:
        """Move a single servo by delegating directly to move_servos."""
        self.move_servos([(servo_id, position)], duration_ms)

    def get_battery_voltage(self) -> int:
        """Send 0x0F request, read response, and return voltage in millivolts."""
        self._write(self.build_frame(0x0F))
        response = self._serial.read(6)
        params = self.parse_response(response, expected_cmd=0x0F)
        return struct.unpack("<H", params[:2])[0]

    def read_servo_positions(self, servo_ids: list[int]) -> dict[int, int]:
        """Send 0x15 to read current positions for a list of servo IDs."""
        count = len(servo_ids)
        params = struct.pack(f"<B{count}B", count, *servo_ids)
        self._write(self.build_frame(0x15, params))

        response = self._serial.read(5 + count * 3)
        params_in = self.parse_response(response, expected_cmd=0x15)

        positions = {}
        num_servos = params_in[0]
        idx = 1
        for _ in range(num_servos):
            s_id = params_in[idx]
            positions[s_id] = struct.unpack("<H", params_in[idx + 1:idx + 3])[0]
            idx += 3
        return positions

    def unload_servos(self, servo_ids: list[int]) -> None:
        """Send 0x14 to disable motor torque on specified servos."""
        count = len(servo_ids)
        params = struct.pack(f"<B{count}B", count, *servo_ids)
        self._write(self.build_frame(0x14, params))

    @staticmethod
    def parse_response(response_bytes: bytes, expected_cmd: int | None = None) -> bytes:
        """Check header, verify echoed command, and return parameter bytes."""
        if len(response_bytes) < 4 or response_bytes[:2] != b"\x55\x55":
            raise ValueError("Invalid LSC frame header")

        length = response_bytes[2]
        cmd = response_bytes[3]

        if len(response_bytes) < 2 + length:
            raise ValueError("Incomplete LSC frame")
        if expected_cmd is not None and cmd != expected_cmd:
            raise ValueError(
                f"Command byte mismatch: expected 0x{expected_cmd:02X}, got 0x{cmd:02X}"
            )
        return response_bytes[4:2 + length]