import numpy as np
from scipy.integrate import odeint

RH=60.
"""
RH float:
    湿度
"""

D=1e-1
"""
D float:
    拡散係数
"""

e_s=1.
"""
e_s float:
    飽和蒸気圧
"""

rho_w=1.
"""
rho_w float:
    水の密度
"""

rho_a=1.
"""
rho_a float:
    空気の密度
"""

gamma = (3 * rho_a) / (8 * rho_w)
"""
gamma float:
    密度比
"""

R_v=1.
"""
R_v float:
    なんかしら
"""

T=1.
"""
T float:
    温度
"""

air=np.array([1.,0.,0.])
"""
air float:
    一様流
"""

g=np.array([0.,0.,-1.])
"""
g float:
    重力ベクトル
"""

def DragCoefficient(v:float):
    """抗力係数

    Args:
        v (float): 飛沫速度

    Returns:
        C_D (float): 抗力係数
    """
    return 1.

coeff_drdt = -(1.- RH/100.) * (D*e_s) / (rho_a*R_v*T)
"""
coeff_drdt float:
    蒸発方程式内に出てくる係数
"""

def differential_equations(var_array:np.ndarray, t) -> np.ndarray:
    """微分方程式
    蒸発と運動を連立
    SciPyのOdeintから呼ばれる想定

    Args:
        var_array (np.ndarray): 時間変化変数配列（半径[0]、速度[1:4]、座標[4:7]）
        t: 時刻

    Returns:
        output (np.ndarray): 微分係数配列
    """
    r:float = var_array[0]
    v:np.ndarray = var_array[1:4]
    x:np.ndarray = var_array[4:7]
    v_r:np.ndarray = air - v
    speed:float = np.linalg.norm(v_r)

    drdt = coeff_drdt / r
    dvdt = g + DragCoefficient(speed) * 0.5*rho_a/r*speed*v_r
    dxdt = v

    output = np.array([drdt])
    output = np.append(output, dvdt)
    output:np.ndarray = np.append(output, dxdt)
    # print(output)
    return output

def velocity_inNextTimeStep(v:np.ndarray, r:float, dt:float) -> np.ndarray:
    """_summary_
        Ruturn velocity in next time step.

    Args:
        v (np.ndarray): velocity in now time step
        r (float): radius in now time step
        dt (float): delta time

    Returns:
        v_n (np.ndarray): velocity in next time step
    """
    v_r:np.ndarray = air - v
    speed:float = np.linalg.norm(v_r)
    C = gamma * DragCoefficient(speed) * speed / r 
    v_n = (v + (g + C*air)*dt) / (1. + C*dt)

    return v_n



if __name__ == '__main__':
    from droplet import get_dropletArray

    droplets = get_dropletArray(1)

    t = np.linspace(0, 5, 201)              #時刻0から5まで、201step刻みで計算する
    droplet = droplets[0]
    y0 = np.hstack([droplets["radius"], droplets["velocity"], droplets["position"]]) #初期値配列（半径[0]、速度[1:4]、座標[4:7]）

    sol = odeint(differential_equations, y0, t)

    print(sol[:, 0])