import sys

input = sys.argv[1]
output = sys.argv[2]

fh = open(input, "r")
fh2 = open(output, "w")


R_type = ["add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and"]
I_type = ["lw", "addi", "sltiu", "jalr"]
S_type = ["sw"]
B_type = ["beq", "bne", "bge", "bgeu", "blt", "bltu"]
U_type = ["auipc", "lui"]
J_type = ["jal"]


instr={
    'add': '0110011', 'sub': '0110011', 'sll': '0110011','slt': '0110011', 'sltu': '0110011', 'xor': '0110011','srl': '0110011', 'or': '0110011', 'and': '0110011',
    'lw': '0000011', 'addi': '0010011', 'sltiu': '0010011','jalr': '1100111',
    'sw': '0100011',
    'beq': '1100011','bne': '1100011', 'blt': '1100011', 'bge': '1100011','bltu': '1100011', 'bgeu': '1100011',
    'lui': '0110111','auipc': '0010111',
    'jal': '1101111'
}
registers= {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}
R_funct7 = {"add": "0000000", "sub": "0100000", "sll": "0000000", "slt": "0000000", "sltu": "0000000", "xor": "0000000", "srl": "0000000", "or": "0000000", "and": "0000000"}

R_funct3 = {"add": "000", "sub": "000", "sll": "001","slt": "010", 'sltu': '011', 'xor': '100','srl': '101', 'or': '110', 'and': '111'}
I_funct3 = {'lw': '010', 'addi': '000', 'sltiu': '011',"jalr": '000'}
S_funct3 = {'sw': "010"}
B_funct3 = {'beq': '000',"bne": '001', 'blt': '100', "bge": '101','bltu': '110', "bgeu": "111"}
def invalid_instr(lst):
    lst1 = ["Invalid Instruction"]
    return "".join(lst1)
def isImmediate(imm):
    if imm[1:].isdigit() == True:
        if int(imm[1:]) >= -2**11 and int(imm[1:]) <= 2**11-1:
            return True
        else:
            return False
    else:
        return False
def decimal_to_twos_complement(num, bits=32):
    max= 2**(bits- 1)-1
    min= -(2**(bits -1))
    if num <min or num >max:
        return "Error: Decimal number out of range for specified bits"
    if num< 0:
        bin_str = bin(num & int("1"*bits, 2))[2:]
    else:
        bin_str = bin(num)[2:].rjust(bits, '0')
    return bin_str

def handle_R (lst):
    lst1=[]
    opcode = instr[lst[0]]
    if opcode not in instr.values():
        return "Invalid opcode"
    funct3 = R_funct3.get(lst[0])
    funct7 = R_funct7.get(lst[0])
    rd= registers.get(lst[1])
    rs1= registers.get(lst[2])
    rs2= registers.get(lst[3])
    if None in (opcode, funct3, funct7, rd, rs1, rs2):
        return "Error: Invalid R-type instruction name or register"
        exit()
    lst1 = [funct7, rs2, rs1, funct3, rd, opcode]
    return ''.join(lst1)

def handle_I(lst):
    lst= lst.replace(",", " ")
    lst1=[]
    opcode = instr.get(lst[0])
    funct3 = I_funct3.get(lst[0])
    if None in (opcode, funct3):
        return "Error: Invalid I-type instruction name or register"
    if lst[0] == "lw":
        imm = lst[2].split('(')[0]
        imm1=str(decimal_to_twos_complement(int(imm)))
        imm2=imm1[::-1]
        rs1 = registers.get(lst[2].split('(')[1][:-1])
        rd = registers.get(lst[1])
    else:
        lst[3] = int(lst[3])
        imm = lst[3]
        imm1=str(decimal_to_twos_complement(int(imm)))
        imm2=imm1[::-1]
        rs1 = registers.get(lst[2])
        rd = registers.get(lst[1])
    isImmediate(imm2)
    if None in (rd, rs1):
        return "Error: Invalid destination or source register"
    lst1= [imm2[11:0:-1], rs1, funct3, rd, opcode]
    return ''.join(lst1)

def handle_S(lst):
    lst1 = []
    opcode = instr[lst[0]]
    if opcode not in instr.values():
        return "Invalid opcode"
    funct3 = S_funct3.get(lst[0])
    if None in (opcode, funct3):
        return "Error: Invalid S-type instruction name or register"
    imm= lst[2].split('(')[0]
    imm1= str(decimal_to_twos_complement(int(imm)))
    imm2= imm1[::-1]
    isImmediate(imm2)
    rs1 = registers.get(lst[2].split('(')[1][:-1])
    rs2 = registers.get(lst[1])
    if None in (rs2, rs1):
        return "Error: Invalid source or base register"
    lst1 = [imm2[11:5:-1], rs2, rs1, funct3, imm2[4:0:-1], opcode]
    return ''.join(lst1)

def handle_B(lst):
    lst1=[]
    opcode= instr.get(lst[0])
    if opcode not in instr.values():
        return "Invalid opcode"
    funct3= B_funct3.get(lst[0])
    rs1= registers.get(lst[1])
    rs2= registers.get(lst[2])
    imm=lst[3]
    imm1=str(decimal_to_twos_complement(int(imm)))
    imm2=imm1[::-1]
    isImmediate(imm2)
    lst1=[imm2[12], imm2[10:5:-1], imm2[5], rs2, rs1, funct3, imm2[4:1:-1], imm2[1], imm2[11], opcode]
    return ''.join(lst1)

def handle_U(lst):
    print(lst[0])
    lst1=[]
    opcode = instr[lst[0]]
    if opcode not in instr.values():
        return "Invalid opcode"
    rd= registers.get(lst[1])
    imm=lst[2]
    imm1= str(decimal_to_twos_complement(int(imm)))
    imm2= imm1[::-1]
    isImmediate(imm2)
    lst1= [imm2[31:12:-1], imm2[12], rd, opcode]
    return ''.join(lst1)

def handle_J(lst):
    lst1=[]
    opcode = instr[lst[0]]
    if opcode not in instr.values():
        return "Invalid opcode"
    rd= registers.get(lst[1])
    imm= lst[2]
    imm1= str(decimal_to_twos_complement(int(imm)))
    imm2 = imm1[::-1]
    isImmediate(imm2)
    lst1= [imm2[20], imm2[10:1:-1], imm2[1], imm2[11], imm2[19:12:-1], imm2[12], rd, opcode]
    return ''.join(lst1)


halt_instr = 'beq zero,zero,0'
def check_length(lst, length):
    if len(lst)!=length:
        return "Error: Length Exceeded"

fininp = [i.strip() for i in fh.readlines()]
for i in fininp:
    if (i == halt_instr):
        fh2.write('00000000000000000000000001100011')
        fh2.write('\n')
        fh2.close()
        exit()
    else:
        i = [x for x in i.replace(',', ' ').split()]

        if (i[0] in R_type):
            check_length(i,4)
            x = handle_R(i)
            fh2.write(x)
            fh2.write('\n')
        elif (i[0] in I_type):
            check_length(i,4)
            x = handle_I(i)
            fh2.write(x)
            fh2.write('\n')
        elif (i[0] in S_type):
            check_length(i, 4)
            x = handle_S(i)
            fh2.write(x)
            fh2.write('\n')
        elif (i[0] in B_type):
            check_length(i,4)
            x = handle_B(i)
            fh2.write(x)
            fh2.write('\n')
        elif (i[0] in U_type):
            check_length(i,3)
            x = handle_U(i)
            fh2.write(x)
            fh2.write('\n')
        elif (i[0] in J_type):
            check_length(i,3)
            x = handle_J(i)
            fh2.write(x)
            fh2.write('\n')
        else:
            x = invalid_instr(i)
            fh2.write(x)
            fh2.write('\n')

fh.close()
fh2.close()