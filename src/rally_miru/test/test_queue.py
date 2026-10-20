# Provided, do not modify.

from rally_miru.instruction_queue import Instruction, InstructionQueue


def make(instruction_id):
    return Instruction(instruction_id, 2, 1)


def test_empty_queue():
    queue = InstructionQueue()
    assert len(queue) == 0
    assert queue.pop() is None


def test_instructions_come_out_in_order():
    queue = InstructionQueue()
    assert queue.add(make(1)) is True
    assert queue.add(make(2)) is True
    assert len(queue) == 2
    assert queue.pop().instruction_id == 1
    assert queue.pop().instruction_id == 2
    assert queue.pop() is None


def test_duplicate_is_ignored():
    queue = InstructionQueue()
    assert queue.add(make(1)) is True
    assert queue.add(make(1)) is False
    assert len(queue) == 1


def test_duplicate_of_a_popped_instruction_is_ignored():
    queue = InstructionQueue()
    queue.add(make(1))
    queue.pop()
    assert queue.add(make(1)) is False
    assert len(queue) == 0


def test_old_id_is_ignored():
    queue = InstructionQueue()
    queue.add(make(1))
    queue.add(make(3))
    assert queue.add(make(2)) is False
    assert [queue.pop().instruction_id, queue.pop().instruction_id] == [1, 3]


def test_id_zero_is_ignored():
    queue = InstructionQueue()
    assert queue.add(make(0)) is False
    assert len(queue) == 0
