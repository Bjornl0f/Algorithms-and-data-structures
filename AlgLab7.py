import numpy as np
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f"{__name__}.log", mode = "w")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")


def straight(a, b): 
    if len(a[0]) != len(b):
        return "Matrices are not m*n and n*p" 
        
    p_matrix = np.zeros((len(a), len(b[0])))
    p_matrix += [[np.sum([a[i][k] * b[k][j] for k in range(len(b))]) for j in range(len(b[0]))] for i in range(len(a))]
    
    return p_matrix
    
    
def split(matrix):  # split matrix into quarters
    row, col = matrix.shape
    
    return matrix[:row//2, :col//2], matrix[:row//2, col//2:], matrix[row//2:, :col//2], matrix[row//2:, col//2:]


def strassen(a, b):
    if len(a) == 1:  # base case: 1x1 matrix
        return a * b
        
    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)
    p1 = strassen(a11 + a22, b11 + b22)  # p1 = (a11 + a22) * (b11 + b22)
    p2 = strassen(a21 + a22, b11)        # p2 = (a21 + a22) * b11
    p3 = strassen(a11, b12 - b22)        # p3 = a11 * (b12 - b22)
    p4 = strassen(a22, b21 - b11)        # p4 = a22 * (b21 - b11)
    p5 = strassen(a11 + a12, b22)        # p5 = (a11 + a12) * b22
    p6 = strassen(a21 - a11, b11 + b12)  # p6 = (a21 - a11) * (b11 + b12)
    p7 = strassen(a12 - a22, b21 + b22)  # p7 = (a12 - a22) * (b21 + b22)
    c11 = p1 + p4 - p5 + p7  # c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5            # c12 = p3 + p5
    c21 = p2 + p4            # c21 = p2 + p4
    c22 = p1 + p3 - p2 + p6  # c22 = p1 + p3 - p2 + p6
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22)))) 
    
    return c
    
    
def check():
    logging.info("Function check started its work")
    a = np.random.randint(0, 10, size=(4, 4))
    b = np.random.randint(0, 10, size=(4, 4))
    assert (strassen(a, b) == straight(a, b)).all()
    assert (np.array(strassen(a, b)) == np.dot(a, b)).all()
    print("Strassen output:")
    logger.info("Strassen function started its work")
    print(*strassen(a, b))
    logger.info("Strassen function ended its work")    

    print("Straight output:")
    logger.info("Straight function started its work")
    print(*straight(a, b))
    logger.info("Straight function ended its work")
    logger.info("Function check() ended its work")
    
    
check()