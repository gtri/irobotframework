*** Keywords ***
Select ${animal} from list
    Open Page    Pet Selection
    Select Item From List    animal_list    ${animal}
