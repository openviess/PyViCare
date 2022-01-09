# based on feedback in: https://github.com/somm15/PyViCare/issues/238

# gas burner and if device has roles "type:heatpump", "type:E3"
def heat_curve_formular_variant1(delta, inside, shift, slope):
    target_supply = (inside + shift - slope * delta
                     * (1.4347 + 0.021 * delta + 247.9
                        * pow(10, -6) * pow(delta, 2)))
    return target_supply


# heatpump has roles "type:heatpump" and with single circuit
def heat_curve_formular_variant2(delta, inside, shift, slope):
    target_supply = (inside + shift - slope * delta
                     * (1.148987 + 0.021 * delta + 247.9
                        * pow(10, -6) * pow(delta, 2)) + 5)
    return target_supply
