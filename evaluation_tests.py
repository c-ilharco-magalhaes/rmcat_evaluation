import matplotlib.pyplot as plt

from link_simulator import LinkSimulator

"""
Evaluation tests for congestion control algorithms.
"""

def ms_to_s(time_ms): return time_ms/1000.0
def s_to_ms(time_s): return time_s*1000.0

def __plot(receiver, times_ms, capacities_kbps):
    """
    Plot results, called at the end of a simulation.
    """
    plt.subplot(311)
    plt.plot(map(ms_to_s, receiver.time_ms), receiver.receiving_rates_kbps, label='receiving rate')
    plt.plot(map(ms_to_s, [0.0]+times_ms), capacities_kbps[0:1]+capacities_kbps,
             label='link capacity', drawstyle='steps')
    plt.ylabel('bitrate (kbps)', fontsize=16)

    plt.subplot(312)
    plt.plot(map(ms_to_s, receiver.time_ms), receiver.delay_signals_ms, label='delay signal')
    plt.ylabel('delay (ms)', fontsize=16)

    plt.subplot(313)
    plt.plot(map(ms_to_s, receiver.time_ms), [100.0*ratio for ratio in receiver.loss_ratios],
             label='loss ratio')
    plt.ylabel('packet loss %', fontsize=16)
    plt.xlabel('time (s)', fontsize=16)
    plt.show()


def __test_single_flow(sender, receiver, times_ms, capacities_kbps, jitter):
    """
    Simulates a RMCAT single flow on a variable capacity link.
    """
    link_simulator = LinkSimulator(None, jitter)
    now_ms = 0.0

    for i in range(len(capacities_kbps)):
        link_simulator.capacity_kbps = capacities_kbps[i]
        end_time_ms = times_ms[i]
        while now_ms < end_time_ms:
            packet = sender.create_packet()
            link_simulator.send_packet(packet)
            if packet.arrival_time_ms is not None:
                receiver.receive_packet(packet)
            feedback = receiver.get_feedback()
            if feedback is not None:
                sender.receive_feedback(feedback)
            now_ms = packet.send_time_ms

    __plot(receiver, times_ms, capacities_kbps)


def rmcat_evaluation_1(sender, receiver, jitter):
    """
    RMCAT Evaluation test 5.1, available here:
    https://tools.ietf.org/html/draft-ietf-rmcat-eval-test-02#section-5.1
    """
    capacities_kbps = [1000.0, 2500.0, 600.0, 1000.0]
    times_ms = map(s_to_ms, [40, 60, 80, 99])
    __test_single_flow(sender, receiver, times_ms, capacities_kbps, jitter)


def test_constant_capacity(sender, receiver, duration_s, capacity_kbps, jitter):
    """
    Simple test for a single flow on a constant capacity testbed.
    """
    __test_single_flow(sender, receiver, [duration_s * 1000.0], [capacity_kbps], jitter)
