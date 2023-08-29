
br = '#664a3a'
bk = '#393637'
wt = '#fff'
tn = '#f6e5d0'
rd = '#b84e45'
mn = '#7c302a'
bl = '#3822ff'
dbl = '#1d0e8e'



pixels = (
    (0, (br, br, br, br, br, br, br)),  # 1
    (-8, (bk, bk, br, br, br, br, br, br, bk, bk, br, br, br, br, br, br, br)),  # 2
    (-10, (bk,) + (br,) * 13 + (bk, bk, br, br, br, bk)),  # 3
    (-11, (br, br, br, br, br, br, br, bk, bk, bk, bk, bk, bk, br, br, br, br, br, bk, br, br, br, bk)),  # 4
    (-12, (br, br, bk, bk, bk, br, br, bk, br, br, br, br, br, br, bk, bk, bk, br, br, br, bk, br, br, bk)),  # 5
    (-9, (bk, br, bk, br, bk) + (br,) * 9 + (bk,) + (br,) * 5 + (bk,)),  # 6
    (-8, (bk,) + (br,) * 4 + (bk, br, br) * 3 + (bk, br, bk) + (br,) * 4),  # 7
    (-8, (br, bk) + (br,) * 4 + (bk, bk, br, bk) + (br,) * 5 + (bk,) + (br,) * 4 + (bk, bk)),  # 8
    (-10, (bk,) * 3 + (br, bk) + (br,) * 3 + (bk, br, br) * 2 + (bk,) + (br,) * 5 + (bk,) + (br,) * 3 + (bk,)),  # 9
    (-10,
     (bk,) + (br,) * 6 + (bk,) + (br,) * 3 + (bk,) + (br,) * 4 + (bk, br, bk, bk, tn, bk) + (br,) * 3 + (bk, br)),
    # 10
    (-11, (
        bk, bk, br, bk, br, br, br, bk, br, br, br, bk, br, br, br, br, bk, br, bk, bk, tn, tn, tn, bk, br, br, br, br,
        bk)),  # 11
    (-12, (
        bk, br, br, bk, br, br, br, br, bk, br, br, br, bk, bk, bk, bk, br, br, bk, tn, tn, tn, tn, tn, tn, bk, br, br,
        br, br, bk)),  # 12
    (-13, (
        br, bk, br, br, br, br, br, br, bk, br, br, br, br, bk, tn, tn, tn, bk, bk, tn, tn, tn, tn, tn, tn, tn, tn, bk,
        br, br, br, br)),  # 13
    (-13, (bk, br, br, bk, br, br, br, bk, br, br, br, br, bk) + (tn,) * 14 + (bk, br, br, bk)),  # 14
    (-13, (bk, br, br, br, br, br, br, bk, br, br, br, bk,) + (tn,) * 16 + (bk, br, br, bk)),  # 15
    (-13, (bk, br, bk, bk, br, br, bk, br, br, br, bk,) + (tn,) * 17 + (bk, br, br, bk)),  # 16
    (-12, (bk, br, br, br, br, bk, br, bk, br, br, bk,) + (tn,) * 16 + (bk, br, br)),  # 17
    (-12, (bk, br, br, br, bk, br, bk, tn, br, bk,) + (tn,) * 10 + (bk, bk, bk, bk, bk, bk, tn, bk, br, br)),  # 18
    (-12, (bk, br, br, bk, br, br, bk) + (tn,) * 19 + (bk, br, br, br)),  # 19
    (-12, (bk, br, bk, br, br, bk, tn, tn, tn, tn, tn, bk, bk, bk, bk, bk, bk) + (tn,) * 10 + (br, br, bk)),  # 20
    (-12, (bk, br, bk, br, br, bk, tn, tn, tn, bk, bk) + (tn,) * 10 + (bk, bk, bk, bk, bk, tn, tn, br, bk)),  # 21
    (-12, (
        bk, br, bk, br, br, bk, tn, tn, tn, tn, tn, bk, bk, bk, bk, bk, tn, tn, tn, tn, tn, wt, br, bk, br, wt, bk, tn,
        br, bk)),  # 22
    (-11, (
        bk, br, bk, br, bk, tn, tn, tn, tn, bk, wt, br, bk, br, wt, tn, tn, tn, tn, tn, wt, br, br, br, wt, wt, tn, bk,
        bk)),  # 23
    (-11, (br, bk, bk, br, bk, tn, tn, tn, bk, wt, wt, br, br, br, wt) + (tn,) * 12 + (bk, tn, bk)),  # 24
    (-11, (br, tn, tn, bk, bk) + (tn,) * 13 + (bk,) + (tn,) * 8 + (bk, tn, bk)),  # 25
    (-11, (bk, tn, bk, br, bk,) + (tn,) * 13 + (bk,) + (tn,) * 8 + (bk, tn, bk)),  # 26
    (-12, (bk, tn, tn, tn, br, bk,) + (tn,) * 14 + (bk,) + (tn,) * 9),  # 27
    (-11, (bk, tn, bk, tn, bk) + (tn,) * 11 + (bk, tn, tn, tn, bk, tn, tn, tn, tn, tn, bk, tn, bk)),  # 28
    (-10, (bk, tn, tn, tn, bk) + (tn,) * 11 + (bk, bk, bk) + (tn, tn, tn, tn, tn, tn, bk, bk)),  # 29
    (-9, (bk, tn, tn, bk) + (tn,) * 20 + (bk,)),  # 30
    (-8, (bk, bk, bk, tn, tn, tn, tn, tn, tn, tn, bk) + (tn,) * 12 + (bk,)),  # 31
    (-5, (bk, tn, tn, tn, tn, tn, tn, tn, bk) + (tn,) * 11 + (bk,)),  # 32
    (-5, (bk, tn, tn, tn, tn, tn, tn, tn, tn, bk, bk, bk, bk, bk, bk, tn, tn, tn, tn, tn, bk)),  # 33
    (-4, (bk,) + (tn,) * 17 + (bk,)),  # 34
    (-4, (bk,) + (tn,) * 16 + (bk,)),  # 35
    (-3, (bk,) + (tn,) * 15 + (bk,)),  # 36
    (-2, (bk,) + (tn,) * 13 + (bk,)),  # 37
    (-1, (bk, bk) + (tn,) * 10 + (bk,)),  # 38
    (0, (bk,) * 13),  # 39
    (0, (bk,) + (tn,) * 8 + (bk, bk, mn, mn, bk, bk)),  # 40
    (0, (bk,) + (tn,) * 6 + (bk, bk, mn, mn, rd, mn, bk, mn, bk, bk, bk, bk)),  # 41
    (0, (bk, mn, bk, bk, bk, bk, mn, rd, rd, rd, rd, rd, mn, bk, mn, bk, rd, mn, mn) + (bk,) * 11 + (mn, mn, bk)),
    # 42
    (-1, (
        bk, mn, mn, bk, rd, rd, bk, rd, rd, rd, rd, rd, mn, mn, bk, mn, bk, rd, rd, mn, rd, bk, rd, rd, rd, rd, rd, rd,
        rd, bk, rd, rd, rd, rd, bk)),  # 43
    (-2, (
        bk, rd, bk, bk, mn, rd, rd, bk, rd, rd, rd, rd, mn, bk, bk, mn, mn, rd, bk, rd, rd, rd, rd, bk, rd, rd, rd, rd,
        rd, bk, rd, bk, rd, rd, rd, rd)),  # 44
    (-4, (
        bk, bk, bk, bk, bk, rd, rd, rd, rd, rd, bk, rd, rd, rd, bk, mn, mn, rd, rd, rd, bk, rd, rd, rd, rd, bk, mn, rd,
        rd, rd, bk, rd, rd, rd, bk, rd, rd, mn)),  # 45
    (-6, (
        bk, rd, bk, rd, bk, rd, bk, bk, rd, rd, rd, rd, bk, rd, bk, bk, bk, mn, rd, rd, rd, rd, bk, bk, rd, rd, rd, rd,
        bk, mn, rd, bk, rd, rd, rd, rd, rd, bk, mn, mn)),  # 46
    (-8, (
        bk, bk, rd, bk, rd, rd, bk, rd, rd, rd, bk, rd, bk, bk, bk, bk, rd, rd, rd, bk, bk, rd, rd, rd, rd, bk, rd, rd,
        rd, rd, rd, bk, mn, bk, rd, rd, rd, rd, rd, rd, bk, mn)),  # 47
    (-10, (
        bk, bk, rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, rd, rd, bk, rd, rd, rd, rd, bk,
        rd, rd, rd, rd, rd, bk, bk, rd, rd, rd, rd, rd, rd, rd, rd, bk)),  # 48
    (-12, (
        bk, bk, rd, bk, rd, bk, rd, rd, rd, rd, bk, rd, rd, mn, bk, rd, rd, rd, rd, bk, rd, rd, rd, rd, bk, rd, rd, rd,
        rd, bk, rd, rd, rd, rd, bk, bk, rd, bk, rd, rd, rd, rd, rd, rd, bk, rd)),  # 49
    (-13, (
        bk, mn, rd, bk, rd, bk, bk, bk, rd, rd, bk, rd, rd, rd, mn, bk, rd, rd, rd, rd, bk, rd, rd, rd, rd, bk, rd, rd,
        rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, rd, rd, bk, mn, rd)),  # 50
    (-14, (
        bk, mn, rd, bk, rd, bk, rd, rd, rd, bk, rd, bk, rd, rd, mn, bk, rd, rd, rd, rd, bk, rd, rd, rd, rd, rd, mn, bk,
        rd, rd, rd, bk, rd, rd, bk, rd, rd, rd, rd, bk, bk, bk, rd, bk, bk, mn, rd, rd)),  # 51
    (-14, (
        bk, mn, bk, rd, rd, bk, rd, rd, rd, rd, bk, rd, rd, rd, mn, bk, rd, rd, rd, rd, bk, rd, rd, rd, rd, rd, mn, mn,
        bk, rd, rd, bk, rd, bk, rd, rd, rd, rd, rd, bk, bk, bk, bk, mn, mn, rd, rd, rd)),
    (-14, (
        bk, mn, bk, rd, rd, bk, rd, rd, rd, rd, bk, rd, rd, rd, mn, bk, rd, rd, rd, rd, bk, rd, rd, rd, rd, bk, rd, rd,
        rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, bk, rd, rd, rd, rd, rd, bk, mn, rd, rd)),
)
