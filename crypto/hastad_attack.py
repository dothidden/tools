#!/usr/bin/env python3
import binascii

# find_mult_inv and nth_root stolen from stack overflow

def find_mult_inv(x, n):
    a = [0, 1]
    q = [None, None]
    r = [n, x]
    i = 1
    
    while r[i] > 1:
        i += 1
        r.append(r[i - 2] % r[i - 1])
        q.append(r[i - 2] // r[i - 1])
        a.append((a[i-2] - q[i] * a[i - 1]) % n)
    
    if r[i] == 1: return a[i]
    else: return None

def mul(l):
    m = 1
    for x in l:
        m *= x
    return m

def list_to_long(l):
    return [int(x, 16) for x in l]

def nth_root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1

# finds x for len(mod_list) modular congruences
def chinese_remainder_theorem(ct_list, mod_list):
    orig_msg = 0

    for ct, mod in zip(ct_list, mod_list):
        rem_mod_list = mod_list.copy()
        rem_mod_list.remove(mod)
        mul_res = mul(rem_mod_list)
        orig_msg += (ct * mul_res * find_mult_inv(mul_res, mod))

    return orig_msg % mul(mod_list)


# decrypts to some HTB flag
ct_list = [
    '536F9C0519E23A35D12DC8D860D0B19821B92CC11852549AFDFED8A196D955CB6604A53A637C6C39B8A5566CD47A1BF231CF68CF2618E1DE8D54577B7BB661CFD85921F3399A19A2382A37D1336D5E07891C4EA3524846875559358DD54BA217E8939BFB42F87F883089FE6C83CBC4A2DED874AD4E6F18FF691BBEE21E1A4471',
    'B78CF3C2EC47ED28CF73598FDC45E8A4D2BA97D56AC7695C693A8B3649470F2B304A7F00F262A6FDAB6A3F18B5CD1560536AEAAAFF56D2309E1ED8DBD8864DA2CB91D4D94EB6AADEDA450F90E447BE88AB4E776B8514AB52DE0AD42BFA4DDC6835F8CA5FFC04A28CD6C89A9E67D71AE82B57B94822C163D355B7FC4D7DDFCBF',
    '4A3B028F1CD454DC388E0CB2EFAAFBD6331DB01D8566B90EB019C6C57E22CE3BE7DEE5398AC141D8D55E0088CC0C9336315AC0320CF466EAE7FF0DCA405D1958B91B4EAD54E848920E5FF9A4D0A12475314AD6C7461B6D8C594C770A4BD8191EEEF7F3D2D40CD14A186BDD5F0CEDF7D1C04E7916E6D37E1CAAEFBDDACD0E04D8',
    '18C915E19D417AF17342B4934CC31674929B276ECDC3623F9D69EE34AB1DDE20D39B919228E1EE3601A2C7FF9D59B2050CCF9A800B6CCEE299398F4C69BF4F7AA952E1740F31E0EB7704A3EABD9B4671099564FA1F876446879102E9A087499031C4FEC8BE690DCA6D32850A6151D2A41B39BD5A03EC5C64338A2787AC6160F2',
    '26D51E82E66578C5F263AE877549AD2DBA1CC00E86B43C1292E67A55DF4EA7945C1EDBC5018FE21B269A87B6B148711A8935DD53DB7EC0B7268051D1C55DC363235C1F07B987CD84FC179BEA901EB0F4D387926FC578D21D06531BA37AF75A2816D51898C68FA3CF6EC7AB67B382FFA2750EA6E861383FD77602C834C14C9009',
]

mod_list = [
    '6C567996A8F7F40DE74536CBBC826BBC8EDCFCE180F5B92EA940F729B5467CE86C7FE9448FBE9CB8AEC42B5B427F9C560F7CA1259D17D8572670B7B55B52BD2FFB750318C18351DB1F111174C9D97D0FDDA5FBB8D762A0C536D924054D60D2810ACEF2FA2D1EC3BB9152CBABBF8AC5765F1A5778B7CEFB53AC3DC87929B55243',
    'BB834511E52FF891A7294F7CDF386A0B9191C90E243F99AC6225E7D8A81C5070DF6FECA313965AD7E129293FFF94090DC19011FEC26407E5FDCF9AA6A067296B39AB2FBCAA0DC02ECF57823FD52440EC3EE0DE29B453B34D9C761C8B2D7C11BDF8C1D12C751199C814B10C26EF637308972AC526EEB40CF76BCDB133E3D2251B',
    '5D27008B6BBF62FA8B5DE80650460ADA5725DA6CED3F923FBA3946D2C7C16A1E0CC3F88594F623C949700FA53232F673F6C23A3F427344573EF2A873EE972ED58FB9F5A22128BDAEDE2A3A2A5F7F0FC03490346CAD83FF26CE215AA9E4A86A20A96067E0251A129D81FCDDBC91DAE5F8EBB0E59653D9DFBB6EB5F926ECB58715',
    '8A47634988EFE6BCDBDD8BEE32EA179BD490920135D4181F0A7085336C51D143B701895BF670F4D7CCAB11AEFC3DE5FF41933B693B1DB0FF58941B6F712DD5175F7924E8059B91A1299B7D52AF6ADDCA21DFA12ED85A61548CDE47AC43B182E89BEC7568D2F32E9905C574F6C27FE3C95870230BA6CFEBB774568CE537215873',
    '9CB7CDC2477FEFBEED0F7F34914E848E8C66EB0A94BBC6A826538837909E7BEE584DBBBD922E5358FC64E94604397A188DAB353AD76CEA8254421102343BE6DFD35E5401AEEF2FA023355A4824CA7FA5A9D095691B481AEF8C0950FB01F1285208651AB531F43010BA8FFED66FE1237562F33974A922394DE8A4C71053A24F95',
]

ct_list = list_to_long(ct_list)
mod_list = list_to_long(mod_list)

orig_msg = chinese_remainder_theorem(ct_list, mod_list)

dec_msg = nth_root(orig_msg, len(mod_list))
print(dec_msg)
print(hex(dec_msg)[2:])
print(bytes.fromhex(hex(dec_msg)[2:]))



