def heat_curve_formular_boiler(outside, inside, shift, slope):
    delta_outside_inside = (outside - inside)
    target_supply = (inside + shift - slope * delta_outside_inside
                     * (1.4347 + 0.021 * delta_outside_inside + 247.9
                        * pow(10, -6) * pow(delta_outside_inside, 2)))
    return target_supply


def heat_curve_formular_heatpump(outside, inside, shift, slope):
    delta_outside_inside = (outside - inside)
    target_supply = (inside + shift - slope * delta_outside_inside
                     * (1.148987 + 0.021 * delta_outside_inside + 247.9
                        * pow(10, -6) * pow(delta_outside_inside, 2)) + 5)
    return target_supply
