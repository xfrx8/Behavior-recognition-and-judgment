class BooleanVectorCounter:
    def __init__(self, size):
        self.size = size
        self.previous_vector = [False] * size
        self.counters = [0] * size

    def update_vector(self, new_vector):
        if len(new_vector) != self.size:
            raise ValueError("The input vector size does not match the initialized size.")

        # Check if the vector has changed
        if new_vector != self.previous_vector:
            for i in range(self.size):
                # Only count True values
                if new_vector[i]:
                    self.counters[i] += 1

        # Update the previous vector state
        if any(new_vector)!= False:
            self.previous_vector = new_vector.copy()
            # print(self.previous_vector)

    def get_counts(self):
        return self.counters

    def reset_counts(self):
        self.counters = [0] * self.size
        self.previous_vector = [False] * self.size

# Example usage:
# counter = BooleanVectorCounter(6)
#
# # Initial vector
# initial_vector = [False, False, False, False, False, False]
# counter.update_vector(initial_vector)
# print(counter.get_counts())  # Output: [0, 0, 0, 0, 0, 0]
#
# # Update with a new vector
# new_vector = [True, False, True, False, False, False]
# counter.update_vector(new_vector)
# print(counter.get_counts())  # Output: [1, 0, 1, 0, 0, 0]
#
# # Another update with the same vector
# same_vector = [True, False, True, False, False, False]
# counter.update_vector(same_vector)
# print(counter.get_counts())  # Output: [1, 0, 1, 0, 0, 0]
#
# # Another update with a dif
