import argparse
import re
import shlex
import math as m
import sys
import atexit
import time
from datetime import datetime
from argparse import ArgumentError
import pygame
from pathlib import Path
from Instructions import SCHEMA
import numpy as np
import ast
import random

# --- Constants & Config ---
SCREEN_W       = 1920
SCREEN_H       = 1080
FPS            = 60
STEPS_PER_TICK = 50
REG_COUNT      = 8192

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='Selects the assembly file')
parser.add_argument('-v', '--verbose', action='store_true',help='Includes verbose messages for debugging')
parser.add_argument('-l', '--logger', action='store_true',help='Sends logs to ~/logs/')
args = parser.parse_args()

class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'a', encoding='utf-8')
        atexit.register(self.cleanup)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def cleanup(self):
        self.log.close()

if args.logger:
    logger = TeeLogger(f"{Path(__file__).parent}/logs/{str(datetime.now()).replace(' ', '')}.log")
    sys.stdout = logger
    sys.stderr = logger

#  Memory / Stack

class Mem:
    """Fixed-size register file. Address 0 is read-only (zero register)."""

    def __init__(self, count: int, zero_addr: bool = True):
        self._mem   = [0] * count
        self._count = count
        self._zero  = zero_addr

    def _check(self, key: int):
        if key >= self._count:
            raise IndexError(f"Register {key} out of range 0-{self._count - 1}")

    def __getitem__(self, key: int):
        self._check(key)
        return self._mem[key]

    def __setitem__(self, key: int, value):
        if key == 0 and self._zero:
            return
        self._check(key)
        self._mem[key] = value


class Stack:
    """Simple call stack for subroutine return addresses."""

    def __init__(self):
        self._stack = []

    def push(self, value: int):
        self._stack.append(value)

    def pop(self):
        self._stack.pop()

    def value(self) -> int:
        return self._stack[-1]

# --- Assembler Logic ---

def load_program(path: str) -> list[str]:
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()] # Skip empty lines

def build_label_table(program: list[str]) -> dict[str, int]:
    return {line: i for i, line in enumerate(program) if line.startswith(':')}

def resolve_arg(arg: str, labels: dict[str, int]) -> str:
    if arg.startswith(':'):
        return str(labels[arg])
    if re.match(r'^r\d+$', arg):
        return re.sub(r'r(\d+)', r'reg[\1]', arg)
    try:
        float(arg)
        return arg
    except ValueError:
        return repr(arg)

def assemble_line(line: str, labels: dict[str, int]) -> str:
    if line.startswith(':'):
        return f"# {line.lstrip(':')}"
    try:
        parts = shlex.split(line)
    except ValueError:
        parts = line.split()
    if not parts: return "pass"
    op   = parts[0].lower()
    args = [resolve_arg(a, labels) for a in parts[1:]]
    return SCHEMA[op].format(*args)

def assemble(program: list[str], labels: dict[str, int]) -> list[str]:
    return [assemble_line(line, labels) for line in program]

# --- VM Execution ---

def run(bytecode: list[str], screen: pygame.Surface, clock: pygame.time.Clock):
    env = {
        'pc'     : 0,
        'running': True,
        'reg'    : Mem(REG_COUNT, zero_addr=True),
        'stack'  : Stack(),
        'screen' : screen,
        'pygame' : pygame,
        'm'      : m,
        'np'     : np,
        'time'   : time,
        'STEPS_PER_TICK' : STEPS_PER_TICK,
        'ast'    : ast,
        'random' : random,
    }

    while env['running']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env['running'] = False

        for _ in range(int(env['STEPS_PER_TICK'])):
            pc = env['pc']
            if pc >= len(bytecode):
                env['running'] = False
                break
            try:
                exec(bytecode[pc], env)
                env['pc'] += 1
            except Exception as e:
                print(f"VM Error at PC {pc}: {e}")
                env['running'] = False
                break
        clock.tick(FPS)

# --- New Importable Function ---

def run_assembly(file: str, verbose: bool = False, logging: bool = False):
    """
    Assembles and executes an assembly file.
    """
    # Handle Logging
    if logging:
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        logger = TeeLogger(f"{log_dir}/{str(datetime.now()).replace(' ', '_').replace(':', '-')}.log")
        sys.stdout = logger
        sys.stderr = logger

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(f"AsmBlur VM - {file}")
    clock = pygame.time.Clock()

    try:
        # Assemble
        program  = load_program(file)
        labels   = build_label_table(program)
        bytecode = assemble(program, labels)

        if verbose:
            print(f"--- Debug Info ---")
            print(f"Labels: {labels}")
            print(f"Bytecode: {bytecode}\n")

        # Execute
        run(bytecode, screen, clock)

    finally:
        pygame.quit()

# --- Main Entry Point (for CLI usage) ---

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', help='Selects the assembly file')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--logger', action='store_true')
    args = parser.parse_args()

    if args.file:
        run_assembly(args.file, args.verbose, args.logger)
    else:
        print("Error: No file path provided. Use -f <path>")