
class AluResult:
    def __init__(self, value, carry, half_carry, zero):
        self.value = value
        self.carry = carry
        self.half_carry = half_carry
        self.zero = zero


def perform_addition_8bit(left, right):
    new_value = (left & 0x0FF) + (right & 0x0FF)
    half_carry = (((left & 0x0F) + (right & 0x0F)) & 0x10) == 0x10
    carry = (new_value & 0x100) == 0x100
    new_value = new_value & 0x0FF
    return AluResult(new_value, carry, half_carry, new_value == 0)


def perform_addition_16bit(left, right):
    new_value = (left & 0x0FFFF) + (right & 0x0FFFF)
    half_carry = (((left & 0x0FFF) + (right & 0x0FFF)) & 0x1000) == 0x1000
    carry = (new_value & 0x10000) == 0x10000
    new_value = new_value & 0x0FFFF
    return AluResult(new_value, carry, half_carry, new_value == 0)


def perform_subtraction_16bit(left, right):
    new_value = (left & 0x0FFFF) - (right & 0x0FFFF)
    half_carry = (((left & 0x0FFF) + (right & 0x0FFF)) & 0x1000) == 0x1000
    carry = (new_value & 0x10000) == 0x10000
    new_value = new_value & 0x0FFFF
    return AluResult(new_value, carry, half_carry, new_value == 0)