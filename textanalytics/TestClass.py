import math

def areaOfTriangle(K, L, M, N, P, Q, R, S):
    area = abs(N - L)*abs(M - K)+abs(S - Q)*abs(R - P);
    if (max(K, P) < min(M, R) and max(L, Q) < min(N, S)) :
        area = area - (min(M, R) - max(K, P))*(min(N, S) - max(L, Q));
    return area;


if __name__== "__main__":
    print("HKHR")
    #area = areaOfTriangle(2, 1, 5, 5, 3, 2, 5, 7)
    #area = areaOfTriangle(2, 2, 5, 7, 3, 4, 6, 9)
    area = areaOfTriangle(-4, 1, 2, 6, 0, -1, 4, 3)
    print("HKHR: AREA : ", area)
