'''
For NGS data analysis test
Usage: generating sequences in FASTA format
Python version: 3.8
Author: @y2mk1ng
'''
import random
def fasta_generator(inp_number):
    f = open('test.fasta', 'w')
    for num in range(0, inp_number):
        line1 = '>test_sequence_number_' + str(num + 1) + '\n'
        lower = ''.join(random.choice('atgc') for i in range(0, 8))
        upper = ''.join(random.choice('ATGC') for j in range(0, 7))
        line2 = '^NN' + lower + upper
        seq = line1 + line2
        print(seq)
        f.write('%s\n' % seq)
    f.close()

def test_main():
    inp_number = int(input('How many seqences do you want: '))
    fasta_generator(inp_number)

if __name__ == '__main__':
    test_main()
