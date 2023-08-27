import argparse
from Bio import SeqIO
import multiprocessing
from itertools import product
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend to prevent X11 window creation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def get_args():
    parser = argparse.ArgumentParser(description='VariaMotif for motif scanning')
    
    # Extract sequences arguments
    parser.add_argument('-extract_sequences', '--extract_sequences', action="store_true", help='extract promoter or orf sequences')
    parser.add_argument("-fna", "--fna", type=str, help="Input FNA file")
    parser.add_argument("-gff", "--gff", type=str, help="Input GFF file")
    parser.add_argument("-up", "--upstream", dest="upstream", type=int, default=400, help="Gene start location upstream length (optional, default is 400)")
    parser.add_argument("-down", "--downstream", dest="downstream", type=int, default=0, help="Gene start location downstream length (optional, default is 0)")
    parser.add_argument("--promoter", dest="promoter", action="store_true", help="Extract promoters")
    parser.add_argument("--orf", dest="orf", action="store_true", help="Extract ORFs")
    
    # VariaMotif arguments
    parser.add_argument('-VariaMotif', '--VariaMotif', action="store_true", help='motif scanning')
    parser.add_argument('-f', '--fasta', type=str, help='FASTA file path')
    parser.add_argument('-motif1', type=str, help='motif1')
    parser.add_argument('-motif2', default="None", type=str, help='motif2, default="None"')
    parser.add_argument('-min_g', '--min_gap', default=0, type=int, help='min gap length between motif1 and motif2')
    parser.add_argument('-max_g', '--max_gap', default=50, type=int, help='max gap length between motif1 and motif2')
    parser.add_argument('-m', '--mismatches', default=0, type=int, help='max mismatches')
    parser.add_argument('-d', '--direction', type=str, default='+', choices=['+,-', '+', '-'], help='Search direction: both, forward (default), or reverse')
    parser.add_argument('-fix', action="store_true", help="For fixed length motif")
    parser.add_argument('-variable', action="store_true", help="For variable length motif")
    
    # Variable motif type arguments
    parser.add_argument('-DNA', action="store_true", help="For DNA variable motif")
    parser.add_argument('-RNA', action="store_true", help="For RNA variable motif")
    parser.add_argument('-protein', action="store_true", help="For protein variable motif")
    # Output arguments
    parser.add_argument('-o', '--output', type=str, help='Output file for motif scanning result and Output file prefix for display')
    
    # VisualMotif arguments
    parser.add_argument('-VisualMotif', '--VisualMotif', action="store_true", help='Display motif in sequence')
    parser.add_argument('-i', '--image', action="store_true", help='Display motif in sequence')
    parser.add_argument('-r', '--display_both_directions', action='store_true', help='Display motifs from both + and - strands.')
    parser.add_argument('-t', '--table', dest='table_file', help='Input table file.')
    
    return parser.parse_args()

#DNA
def generate_motif_variants(motif):
    variants = []
    ambiguous_bases = {
        'W': 'AT',
        'S': 'GC',
        'M': 'AC',
        'K': 'GT',
        'R': 'AG',
        'Y': 'CT',
        'B': 'CGT',
        'D': 'AGT',
        'H': 'ACT',
        'V': 'ACG',
        'N': 'ACGT'
    }
    variant_bases = []
    motif_variants = []

    for base in motif:
        if base in ambiguous_bases:
            variant_bases.append(list(ambiguous_bases[base]))
        else:
            variant_bases.append([base])

    motif_variants = product(*variant_bases)

    for variant in motif_variants:
        variants.append(''.join(variant))

    return variants

def calculate_mismatches(fragment, variants):
    mismatches_list = []

    for variant in variants:
        mismatches = 0
        for base, variant_base in zip(fragment, variant):
            if variant_base not in base:
                mismatches += 1
        mismatches_list.append(mismatches)

    return min(mismatches_list)


def search_motif(record, motif, max_mismatches, motif_length):
    variants = generate_motif_variants(motif)
    sequence = str(record.seq)
    sequence_length = len(sequence)

    results = []

    for i in range(sequence_length - motif_length + 1):
        fragment = sequence[i:i+motif_length]
        mismatches = calculate_mismatches(fragment, variants)
        
        if mismatches <= max_mismatches:
            result = {
                'motif': motif,
                'sequence_length':sequence_length,
                'sequence_id': record.id,
                'start': i,
                'end': i + motif_length - 1,
                'mismatches': mismatches,
                'fragment': fragment,
                'strand': '+',
            }
            results.append(result)

    return results
	
def reverse_search(record, motif, max_mismatches, motif_length):
    variants = generate_motif_variants(motif)
    sequence = str(record.seq.reverse_complement())
    motif_length = len(motif)
    sequence_length = len(sequence)
    results = []

    for i in range(sequence_length - motif_length + 1):
        fragment = sequence[i:i+motif_length]
        mismatches = calculate_mismatches(fragment, variants)

        if mismatches <= max_mismatches:
            result = {
                'motif': motif,
                'sequence_length':sequence_length,
                'sequence_id': record.id,
                'start': i,
                'end': i + motif_length - 1,
                'mismatches': mismatches,
                'fragment': fragment,
                'strand': '-',
            }
            results.append(result)

    return results
def reverse_search_fix(record, motif, max_mismatches, motif_length):
    variants = generate_motif_variants(motif)
    sequence = str(record.seq.reverse_complement())
    motif_length = len(motif)
    sequence_length = len(sequence)
    results = []

    for i in range(sequence_length - motif_length + 1):
        fragment = sequence[i:i+motif_length]
        mismatches = calculate_mismatches(fragment, variants)

        if mismatches <= max_mismatches:
            result = {
                'motif': motif,
                'sequence_length':sequence_length,
                'sequence_id': record.id,
                'start': sequence_length - i - motif_length,
                'end': sequence_length - i - 1,
                'mismatches': mismatches,
                'fragment': fragment,
                'strand': '-',
            }
            results.append(result)

    return results	

#protein
def calculate_mismatche_protein(fragment, motif):
    mismatches = 0
    for aa, motif_aa in zip(fragment, motif):
        if motif_aa == 'X':  # Wildcard symbol, any amino acid is allowed
            continue
        if motif_aa != aa:
            mismatches += 1
    return mismatches

def search_motif_protein(record, motif, max_mismatches, motif_length):
    sequence = str(record.seq)
    sequence_length = len(sequence)

    results = []

    for i in range(sequence_length - motif_length + 1):
        fragment = sequence[i:i+motif_length]
        mismatches = calculate_mismatche_protein(fragment,motif)
        
        if mismatches <= max_mismatches:
            result = {
                'motif': motif,
                'sequence_id': record.id,
                'sequence_length':sequence_length,
                'start': i,
                'end': i + motif_length - 1,
                'mismatches': mismatches,
                'fragment': fragment,
                'strand': '+',
            }
            results.append(result)

    return results


#combine	
def combine_results_forward(record, motif1_results_chunk, motif2_results,max_mismatches, min_gap, max_gap):
    sequence = str(record.seq)
    sequence_length = len(sequence)
    sequence_id = record.id
    combined_results = []
    
    for motif1_result in motif1_results_chunk:
        for motif2_result in motif2_results:
            gap_length = motif2_result['start'] - motif1_result['end'] - 1
            if gap_length > max_gap:
                break
            if motif1_result['end'] < motif2_result['start'] and motif1_result['mismatches'] + motif2_result['mismatches'] <= max_mismatches and min_gap <= gap_length <= max_gap:
                combined_result = {
                    'sequence_id': sequence_id,
                    'sequence_length': sequence_length,
                    'motif': motif1_result['motif'] + ',' + motif2_result['motif'],
                    'start': motif1_result['start'],
                    'end': motif2_result['end'],
                    'strand': motif1_result['strand'],
                    'motif1_mismatch': motif1_result['mismatches'],
                    'fragment1': motif1_result['fragment'],
                    'motif2_mismatch': motif2_result['mismatches'],
                    'fragment2': motif2_result['fragment'],
                    'mismatch': motif1_result['mismatches'] + motif2_result['mismatches'],
                    'gap_length': gap_length,
                    'sequence': sequence[motif1_result['start']:motif2_result['end'] + 1]
                }
                combined_results.append(combined_result)
    
    return combined_results

def combine_results_reverse(record, motif1_results_chunk, motif2_results,max_mismatches, min_gap, max_gap):
    sequence = str(record.seq.reverse_complement())
    sequence_length = len(sequence)
    sequence_id = record.id
    combined_results = []
    
    for motif1_result in motif1_results_chunk:
        for motif2_result in motif2_results:
            gap_length = motif2_result['start'] - motif1_result['end'] - 1
            if gap_length > max_gap:
                break
            if motif1_result['end'] < motif2_result['start'] and motif1_result['mismatches'] + motif2_result['mismatches'] <= max_mismatches and min_gap <= gap_length <= max_gap:
                combined_result = {
                    'sequence_id': sequence_id,
                    'sequence_length': sequence_length,
                    'motif': motif1_result['motif'] + ',' + motif2_result['motif'],
                    'start': sequence_length - motif2_result['end'] -1,
                    'end': sequence_length - motif1_result['start'] -1,
                    'strand': motif1_result['strand'],
                    'motif1_mismatch': motif1_result['mismatches'],
                    'fragment1': motif1_result['fragment'],
                    'motif2_mismatch': motif2_result['mismatches'],
                    'fragment2': motif2_result['fragment'],
                    'mismatch': motif1_result['mismatches'] + motif2_result['mismatches'],
                    'gap_length': gap_length,
                    'sequence': sequence[motif1_result['start']:motif2_result['end'] + 1]
                }
                combined_results.append(combined_result)
    
    return combined_results

def plot_motifs_to_single_chart(file_path, output_file, display_both_directions=False):
    df = pd.read_csv(file_path, sep='\t', header=None, dtype={0: str, 1: int, 2: str, 3: int, 4: int, 5: str}, usecols=[0, 1, 2, 3, 4, 5], skiprows=1, names=["Sequence ID", "Length", "Motif", "Start", "End", "Strand"])

    grouped_df = df.groupby("Sequence ID")

    num_sequences = len(grouped_df)
    height_interval = 0.5
    max_length = df["Length"].max()
    line_length = 15
    multiplier = line_length / max_length

    fig, ax = plt.subplots(figsize=(line_length, num_sequences * 0.5))
    ax.axis('off')


    color_list = ['#008000','#FF0000', '#0000FF', '#FF00FF', '#00FFFF', '#FFFF00', '#800000', '#00FF00', '#000080', '#808000', '#800080', '#008080', '#808080', '#C0C0C0', '#FFA500']
    color_map = {}

    first_line_position = None
    first_seq_id = None
    for idx, (seq_id, seq_group) in enumerate(grouped_df):
        y_position = idx * 2
        seq_length = seq_group.iloc[0]["Length"]
        line = seq_length * multiplier
        ax.plot([0, line], [y_position, y_position], color='black')
        ax.text(-0.5, y_position, seq_id, ha='right', va='center', fontsize=10)

        first_sequence_y = y_position
        first_seq_id = seq_id
  
        for _, row in seq_group.iterrows():
            start = row["Start"]
            end = row["End"]
            direction = row["Strand"]
            motif = row["Motif"]
            arrow_length = (end-start)*line_length/max_length*0.2
            shift_amount = arrow_length

            if not display_both_directions and direction == '-':
                continue

            motif_length = end - start

            if motif not in color_map:
                color_map[motif] = color_list[len(color_map) % 15]

            color = color_map[motif]

            if direction == '+':
                rectangle = plt.Rectangle((start / seq_length * line, y_position), (end - start) / seq_length * line, height_interval, facecolor=color, edgecolor='none')
            else:  # direction == '-'
                rectangle = plt.Rectangle(((start - shift_amount) / seq_length * line, y_position), (end - start) / seq_length * line, height_interval, facecolor=color, edgecolor='none')

            ax.add_patch(rectangle)

            if direction == '+':
                arrow_tail_x = (start + motif_length - shift_amount) / seq_length * line
                arrow_head_x = arrow_tail_x + arrow_length
            else:  # direction == '-'
                arrow_tail_x = (start + shift_amount) / seq_length * line
                arrow_head_x = arrow_tail_x - arrow_length

            arrow_polygon = np.array([[arrow_head_x, y_position + height_interval / 2], [arrow_tail_x, y_position], [arrow_tail_x, y_position + height_interval]])
            arrow = plt.Polygon(arrow_polygon, closed=True, edgecolor=color, facecolor=color)
            ax.add_patch(arrow)
    #
    y_pos = first_sequence_y + 2
    ax.plot([0, line_length], [y_pos, y_pos], color='black')

    tick_positions = np.linspace(0, line_length, num=11)
    tick_labels = np.linspace(0, max_length, num=11, dtype=int)
    for tick_pos in tick_positions:
        ax.plot([tick_pos, tick_pos], [y_pos, y_pos - 0.2], color='black')
    for tick_pos, tick_label in zip(tick_positions, tick_labels):
        ax.text(tick_pos, y_pos - 1.2 , str(tick_label), ha='center', va='bottom', fontsize=10)



    ax.set_xlim(0, line_length) 
    ax.set_ylim(-1, num_sequences * 2)
    ax.set_xticks(np.arange(0, line_length + 1))
    ax.set_xlabel('Position (cm)')
    ax.set_title('Motif Search Results', fontweight='bold')
    ax.set_yticks([])

    legend_elements = [Patch(facecolor=color, edgecolor='black', label=motif) for motif, color in color_map.items()]
    ax.legend(handles=legend_elements, title='Motif', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    #Save as PDF 
    output_file_pdf = f'{output_file}.pdf'
    plt.savefig(output_file_pdf, bbox_inches='tight',format='pdf')

    #Save as PNG
    output_file_png = f'{output_file}.png'
    plt.savefig(output_file_png, bbox_inches='tight',format='png')

def process_record_protein(record, motif1, motif2, max_mismatches, min_gap, max_gap):
    motif1_results = search_motif_protein(record, motif1, max_mismatches, len(motif1))
    motif2_results_pre = search_motif_protein(record, motif2, max_mismatches, len(motif2))
    motif2_results = sorted(motif2_results_pre, key=lambda x: x['start'])
    combined_results = combine_results_forward(record, motif1_results, motif2_results, max_mismatches, min_gap, max_gap)
    return combined_results

def process_record_DNA_forward(record, motif1, motif2, max_mismatches, min_gap, max_gap):
    motif1_results = search_motif(record, motif1, max_mismatches, len(motif1))
    motif2_results_pre = search_motif(record, motif2, max_mismatches, len(motif2))
    motif2_results = sorted(motif2_results_pre, key=lambda x: x['start'])
    combined_results = combine_results_forward(record, motif1_results, motif2_results, max_mismatches, min_gap, max_gap)
    return combined_results

def process_record_DNA_reverse(record, motif1, motif2, max_mismatches, min_gap, max_gap):
    motif1_results = reverse_search(record, motif1, max_mismatches, len(motif1))
    motif2_results_pre = reverse_search(record, motif2, max_mismatches, len(motif2))
    motif2_results = sorted(motif2_results_pre, key=lambda x: x['start'])
    combined_results = combine_results_reverse(record, motif1_results, motif2_results, max_mismatches, min_gap, max_gap)
    return combined_results

def calculate_average_length(sequence_file):
    total_length = 0

    sequence_count = 0
    
    for record in SeqIO.parse(sequence_file, "fasta"):  # 假设文件格式是fasta格式
        total_length += len(record.seq)
        sequence_count += 1
    
    if sequence_count == 0:
        return 0  # Handle the case of an empty file
    
    average_length = total_length / sequence_count
    return average_length


def main():
    args = get_args()
    fasta_file_path = args.fasta
    motif1 = args.motif1
    motif2 = args.motif2
    max_mismatches = args.mismatches
    min_gap = args.min_gap
    max_gap = args.max_gap
    direction = args.direction
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    if args.VariaMotif:
        records = list(SeqIO.parse(fasta_file_path, "fasta"))
        all_results = []
        if args.fix:
            if args.DNA or args.RNA:
                if direction == '+' or direction == '+,-':
                    motif1_results = pool.starmap(search_motif, [(record, motif1, max_mismatches, len(motif1)) for record in records])
                    motif1_results = [item for sublist in motif1_results for item in sublist]
                    all_results.extend(motif1_results)
                if direction == '-' or direction == '+,-':
                    motif1_results = pool.starmap(reverse_search_fix, [(record, motif1, max_mismatches, len(motif1)) for record in records])
                    motif1_results = [item for sublist in motif1_results for item in sublist] #Flatten the list
                    all_results.extend(motif1_results)


            if args.protein:
                motif1_results = pool.starmap(search_motif_protein, [(record, motif1, max_mismatches, len(motif1)) for record in records])
                motif1_results = [item for sublist in motif1_results for item in sublist] 
                all_results.extend(motif1_results) 

  
            if not all_results:
                print("#No Result")
            else:
                with open(args.output,'w') as output_file:
                    output_file.write("Sequence_ID\tSequence_Length\tmotif\tstart\tend\tstrand\tmismatches\tmatched_sequence\n")
                    for result in all_results:
                        output_file.write(f"{result['sequence_id']}\t{result['sequence_length']}\t{result['motif']}\t{result['start']}\t{result['end']}\t{result['strand']}\t{result['mismatches']}\t{result['fragment']}\n")
        if args.variable:
            if args.DNA or args.RNA:

                if calculate_average_length(fasta_file_path) > 2000:
                    for record in records:
                        if direction == '+' or direction == '+,-':
                            motif1_results = search_motif(record, motif1, max_mismatches, len(motif1))
                            motif2_results_pre = search_motif(record, motif2, max_mismatches, len(motif2))
                            motif2_results = sorted(motif2_results_pre, key=lambda x: x['start'])
                            num_chunks = multiprocessing.cpu_count()
                            chunk_size = max(len(motif1_results) // num_chunks,1)
                            chunks = [motif1_results[i:i + chunk_size] for i in range(0, len(motif1_results), chunk_size)]
                            combined_results = pool.starmap(combine_results_forward, [(record, motif1_results_chunk, motif2_results, max_mismatches, min_gap, max_gap) for motif1_results_chunk in chunks])
                            combined_results = [item for sublist in combined_results for item in sublist]
                            all_results.extend(combined_results)			
                        if direction == '-' or direction == '+,-':
                            motif1_results = reverse_search(record, motif1, max_mismatches, len(motif1))
                            motif2_results_pre = reverse_search(record, motif2, max_mismatches, len(motif2))
                            motif2_results = sorted(motif2_results_pre, key=lambda x: x['start'])
                            num_chunks = multiprocessing.cpu_count()
                            chunk_size = max(len(motif1_results) // num_chunks,1)
                            chunks = [motif1_results[i:i + chunk_size] for i in range(0, len(motif1_results), chunk_size)]
                            combined_results = pool.starmap(combine_results_reverse, [(record, motif1_results_chunk, motif2_results, max_mismatches, min_gap, max_gap) for motif1_results_chunk in chunks])
                            combined_results = [item for sublist in combined_results for item in sublist]
                            all_results.extend(combined_results)
                else:
                    if direction == '+' or direction == '+,-':
                        combined_results = pool.starmap(process_record_DNA_forward, [(record, motif1, motif2, max_mismatches, min_gap, max_gap) for record in records])
                        combined_results = [item for sublist in combined_results for item in sublist] #Flatten the list
                        all_results.extend(combined_results)
			
                    if direction == '-' or direction == '+,-':
                        combined_results = pool.starmap(process_record_DNA_reverse, [(record, motif1, motif2, max_mismatches, min_gap, max_gap) for record in records])
                        combined_results = [item for sublist in combined_results for item in sublist] #Flatten the list
                        all_results.extend(combined_results)               


            if args.protein:
                combined_results = pool.starmap(process_record_protein, [(record, motif1, motif2, max_mismatches, min_gap, max_gap) for record in records])
                combined_results = [item for sublist in combined_results for item in sublist] #Flatten the list
                all_results.extend(combined_results)

            if not all_results:
                print("# No Result")
            else:
                with open(args.output, 'w') as output_file:
                    output_file.write("Sequence_ID\tSequence_Length\tMotif\tstart\tend\tstrand\tmotif1_mismatch\tfragment1\tmotif2_mismatch\tfragment2\tmismatches\tgap_length\tmatched_sequence\n")
                    for result in all_results:
                        output_file.write(f"{result['sequence_id']}\t{result['sequence_length']}\t{result['motif']}\t{result['start']}\t{result['end']}\t{result['strand']}\t{result['motif1_mismatch']}\t{result['fragment1']}\t{result['motif2_mismatch']}\t{result['fragment2']}\t{result['mismatch']}\t{result['gap_length']}\t{result['sequence']}\n")

        if args.image:
            plot_motifs_to_single_chart(args.output, args.output, display_both_directions=args.display_both_directions)

    if args.VisualMotif:
        plot_motifs_to_single_chart(args.table_file, args.output, args.display_both_directions)

    if args.extract_sequences:
        # Read FNA file and create a dictionary of sequences
        sequences = SeqIO.to_dict(SeqIO.parse(args.fna, "fasta"))

        # Open output file for writing
        output_handle = open(args.output, "w")

        # Process GFF file
        with open(args.gff, "r") as gff_handle:
            for line in gff_handle:
                line = line.strip()
                if line.startswith("#"):
                    continue

                fields = line.split("\t")
                feature_type = fields[2]
                strand = fields[6]

                if feature_type == "CDS":
                    seq_name = fields[0]
                    seq_start = int(fields[3])
                    seq_end = int(fields[4])
                    attributes = fields[8].split(";")
                    cds_id = parent = gene = product = "None"

                    for attr in attributes:
                        if attr.startswith("ID="):
                            cds_id = attr[3:]
                        elif attr.startswith("Parent="):
                            parent = attr[7:]
                        elif attr.startswith("gene="):
                            gene = attr[5:]
                        elif attr.startswith("product="):
                            product = attr[8:]

                    if seq_name in sequences:
                        sequence = sequences[seq_name].seq
                        if args.promoter:
                            if strand == "-":
                                start = max(seq_end - args.downstream, 0)
                                end = start + args.upstream + args.downstream
                                seq_fragment = sequence[start:end].reverse_complement()
                            else:
                                start = max(seq_start - args.upstream, 0)
                                end = start + args.upstream + args.downstream
                                seq_fragment = sequence[start:end]
                        elif args.orf:
                            if strand == "-":
                                seq_fragment = sequence[seq_start - 1:seq_end].reverse_complement()
                            else:
                                seq_fragment = sequence[seq_start - 1:seq_end]
                        else:
                            continue

                        seq_record = SeqRecord(seq_fragment, id=f"{seq_name}|{cds_id}|{parent}|{gene}|{seq_start}|{seq_end}|{strand}|{product}",description="")
                        SeqIO.write(seq_record, output_handle, "fasta")

        # Close output file
        output_handle.close()
if __name__ == "__main__":
    main()

