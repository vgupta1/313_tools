def sensitivity_analysis(model):

    import pandas as pd
    
    # OBJECTIVE SENSITIVITY

	# for each variable in the moel, determine
	# - variable name
	# - final value
	# - reduced cost
    # - objective coefficient
    # - allowable increase
    # - allowable decrease

    variable_names = []
    final_values = []
    reduced_costs = []
    objective_coefficients = []
    allowable_increase = []
    allowable_decrease = []

    for v in model.getVars():
        variable_names.append(v.varName)
        final_values.append(v.x)
        reduced_costs.append(v.RC)
        objective_coefficients.append(v.obj)
        allowable_increase.append(v.SAObjUp)
        allowable_decrease.append(v.SAObjLow)
        
    # the two following changes make the constraint sensitivity analysis match the output of the solver sensitivity report
    for i in range(len(objective_coefficients)):
        allowable_increase[i] = allowable_increase[i] - objective_coefficients[i]
        allowable_decrease[i] = objective_coefficients[i] - allowable_decrease[i]


    # create a data frame for a "Variable Cells" table that is indexed by the variable names and has columns: 
    #    final value, reduced cost, objective coefficient, allowable increase, and allowable decrease
    variable_cells = pd.DataFrame(
        {
            "Final Value": final_values,
            "Reduced Cost": reduced_costs,
            "Objective Coefficient": objective_coefficients,
            "Allowable Increase": allowable_increase,
            "Allowable Decrease": allowable_decrease,
        },
        index=variable_names,
    )

    
    # CONSTRAINT SENSTIVITY
    # for each constraint in the moel, determine
    # - constraint name
    # - shadow price
    # - right hand side
    # - allowable increase
    # - allowable decrease
    # - slack value


    constraint_names = []
    shadow_prices = []
    left_hand_sides = []
    right_hand_sides = []
    const_allowable_increase = []
    const_allowable_decrease = []
    slack_values = []

    for c in model.getConstrs():
        if c.ConstrName.lower() != "non-negativity":
            constraint_names.append(c.ConstrName)
            shadow_prices.append(c.Pi)
            left_hand_sides.append(model.getRow(c).getValue())
            right_hand_sides.append(c.RHS)
            const_allowable_increase.append(c.SARHSUp)
            const_allowable_decrease.append(c.SARHSLow)
            slack_values.append(c.slack)    
        

    for i in range(len(right_hand_sides)):
        const_allowable_increase[i] = const_allowable_increase[i] - right_hand_sides[i]
        const_allowable_decrease[i] = right_hand_sides[i] - const_allowable_decrease[i]


    # create a data frame for a "Constraints" table that is indexed by constraint name and has columns: final value, shadow price, constraint RHS, allowable increase, allowable decrease
    constraint_cells = pd.DataFrame(
        {
            "Final Value": left_hand_sides,
            "Shadow Price": shadow_prices,
            "Constr. RHS": right_hand_sides,
            "Allowable Increase": const_allowable_increase,
            "Allowable Decrease": const_allowable_decrease
        },
        index=constraint_names,
    )
    

    # set the pandas option to print all rows of the dataframes
    pd.set_option("display.max_rows", None)

    # set the pandas width option to 400 (you may want to change this for your own computer)
    pd.set_option("display.width", 400)

    # set the float format to a fixed-point number with 6 decimal places
    pd.options.display.float_format = '{:.8f}'.format

    # print the "Variable Cells" table 
    print("Variable Cells")
    print(variable_cells)

    # print a blank line
    print("\n------------------------------------------------------------------------------------\n")

    # print the "Constraints" table
    print("Constraints")
    print(constraint_cells)
