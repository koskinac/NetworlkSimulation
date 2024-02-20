import numpy as np
import matplotlib.pyplot as plt

class NetworkSimulation:
    def __init__(self, num_computers=8, max_queue_size=5):
        # Constructor to initialize the NetworkSimulation object
        self.num_computers = num_computers
        self.max_queue_size = max_queue_size
        self.server_queue = []
        self.bad_slots = []
        self.lost_packets = []

    # Simulates packet transmission in the network for a given probability p
    def transmit(self, p):
        self.server_queue = [[] for _ in range(self.num_computers)]
        bad_slots_count = 0
        total_transmitted_packets = 0
        lost_packets_count = 0

        # Count of the lost packets 
        for slot in range(1000): #Simulate 1000 slots
            for computer in range(self.num_computers):
                if np.random.rand() < p:
                    if len(self.server_queue[computer]) < self.max_queue_size:
                        self.server_queue[computer].append(slot)
                    else:
                        lost_packets_count += 1

            # Calculate if the packets are transmitted normaly or delayed 
            for computer in range(self.num_computers):
                if self.server_queue[computer]:
                    total_transmitted_packets += 1
                    if len(self.server_queue) > 1:
                        bad_slots_count += 1
                        self.bad_slots.append(slot)
                    self.server_queue[computer].pop(0)
                    
        # Calculate length of bad slots and rate of lost packets
        self.bad_slots.append(1000)
        self.bad_slots = np.diff(self.bad_slots).tolist()
        self.lost_packets.append(lost_packets_count / total_transmitted_packets)
        return bad_slots_count, lost_packets_count / total_transmitted_packets
    
    def calcualte_throughput(self, p):
        # Calculates the throughput of the network for a given probability p
        total_transmitted_packets = 0
        for slot in range(1000):
            for computer in range(self.num_computers):
                if np.random.rand() < p:
                    if len(self.server_queue[computer]) < self.max_queue_size:
                        total_transmitted_packets += 1
                        self.server_queue[computer].append(slot)
                    else: 
                        self.server_queue[computer].pop(0)
        return total_transmitted_packets / 1000
    

def plot_graph(x_values, y_values, x_label, y_label, title):
    plt.plot(x_values, y_values, marker='o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    simulation = NetworkSimulation()

    #Part 1: Calculate bad points
    p_values = np.arange(0.1, 1.1, 0.1)
    bad_points = []
    for p in p_values:
        bad_points_count, _ = simulation.transmit(p)
        bad_points.append(bad_points_count)
    plot_graph(p_values, bad_points, 'Peak p ', 'Number of bad points', 'Bad Points vs Peak p')


    #Part 2: Calculate throughput
    throughput_values = []
    for p in p_values:
        throughput = simulation.calcualte_throughput(p)
        throughput_values.append(throughput)
    plot_graph(p_values, throughput_values, 'Peak P', 'Throughput', 'Throughput vs Peak p')

    #Part 3: Calculate rate of lost packets
    lost_packet_rates = []
    for p in p_values:
        _, lost_packet_rate = simulation.transmit(p)
        lost_packet_rates.append(lost_packet_rate)
    plot_graph(p_values, lost_packet_rates, 'Peak p', 'Rate of Lost Packets', 'Rate of lost packets vs Peak p')

           

        
    


        
