# PCP_Assign
Assignment of members to PCPs based on member criteria and PCP performance scores

This Python script assigns members to Primary Care Providers (PCPs) based on geographical proximity, panel restrictions, and matching criteria such as age, gender, and demographic preferences. The updated version introduces address validation for Texas and exception handling for members or PCPs with invalid addresses (i.e., coordinates outside Texas).

Key Features and Updates:
Haversine Formula for Distance Calculation:

The script uses the Haversine formula to compute the distance (in miles) between members and PCPs based on their geographical coordinates (latitude and longitude).
Address Validation (Texas Only):

Both members and PCPs are only considered valid if their addresses (latitude and longitude) fall within the geographical boundaries of Texas (latitude between 25.83 and 36.5, longitude between -106.65 and -93.51).
If a member or PCP is located outside of Texas, they are flagged with an exception.
Panel Restrictions:

PCPs must be accepting new patients and must not have exceeded their panel size limit (the number of patients they can handle). If these conditions are not met, the PCP is excluded from the matching process.
Matching Algorithm:

The algorithm assigns each member to the closest PCP who meets all the following criteria:
Age compatibility (PCP’s age range must match the member’s age).
Gender compatibility (PCP’s gender preference must match the member’s gender or be set to “Any”).
Demographic compatibility (PCP must serve the same demographic area as the member).
The script also penalizes mismatches in these criteria by adding large penalty values to the distance, making incompatible matches less likely.
Exception Handling:

Invalid Addresses: Members or PCPs with invalid addresses (outside of Texas) are flagged with a custom status.
Detailed Logging of Exceptions: Any member or PCP with an invalid address is logged in an exception list, which is displayed at the end of the process.
No Maximum Search Radius:

Matching is constrained by ensuring that both members and PCPs are located within Texas.
Workflow:
Data Generation: The script generates sample data for members and PCPs, including attributes like age, gender, latitude, longitude, and performance scores. Some coordinates are intentionally set outside Texas to test exception handling.

Preprocessing: The script preprocesses categorical fields (e.g., gender, ethnicity) by converting them into numerical representations for easier matching.

Matching Process: For each member, the algorithm searches for the closest valid PCP based on geographical distance and criteria matching. PCPs with invalid addresses or who do not meet the panel restrictions are excluded.

Assignments and Exceptions: Members are assigned to PCPs, and any members or PCPs with invalid addresses are recorded in an exception list.

Outputs:
Member Assignments: Displays the assigned PCP for each member. If no valid match is found or the member’s address is invalid, the output will show “No Match” or “Invalid Address.”
Exception List: Logs and prints details of members or PCPs with invalid addresses (outside Texas).
This update improves the robustness of the assignment process by ensuring that only members and PCPs located in Texas are considered and by handling edge cases like invalid addresses.
