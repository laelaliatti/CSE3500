import imagematrix
import math
import numpy as np
class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True): 
        width = self.width
        height = self.height
        costs = np.array([self.energy(i, 0) for i in range(width)])
        backpointer = np.zeros((width, height), dtype=int)
        if not dp:

            def recursive(i,j):
                if j == height - 1:
                    return self.energy(i,j), ([i,j])
                
                best_cost = math.inf
                best_path = None

                for next_i in [i - 1, i, i + 1]:
                    if 0 <= next_i < width:
                        cost, path = recursive(next_i, j + 1)
                        total_cost = self.energy(i, j) + cost

                        if total_cost < best_cost:
                            best_cost = total_cost
                            best_path = [(i, j)] + path

                return best_cost, best_path
            
            overall_best = math.inf
            overall_path = None

        # Try starting from every pixel in top row
            for i in range(width):
                cost, path = recursive(i, 0)
                if cost < overall_best:
                    overall_best = cost
                    overall_path = path

            return overall_path
        for j in range(1,height):
                # Pre-allocate a new NumPy array for the current row
            new_costs = np.zeros(width)

            for i in range(width):
                # For a vertical seam, these are (i-1, j-1), (i, j-1), (i+1, j-1)
                left = costs[i-1] if i > 0 else np.inf
                    #looks up to left
                mid = costs[i]
                    #looks up and if i is less than zero then it'll return high cost.
                right = costs[i+1] if i < width - 1 else np.inf
                    #looks up to right
                best_val = min(left, mid, right)
                new_costs[i] = self.energy(i, j) + best_val

                #records index of best neighbor for backtracking.
                if best_val == left:
                    backpointer[i, j] = i - 1
                elif best_val == mid:
                    backpointer[i, j] = i
                else:
                    backpointer[i, j] = i + 1
            #updates the costs
            costs = new_costs

        seam = []
            #where is the smallest value
        curr_i = np.argmin(costs)

        for j in range(height - 1, -1, -1):
            seam.append((curr_i, j))
            curr_i = backpointer[curr_i, j]

        #expect the seam from top-to-bottom, so reverse it.
        return seam[::-1]
 
            
            
            
