*** Settings ***
Documentation     Highlight Robot Syntax
Suite Setup       Make a Highlighting Notebook
Default Tags      kernel:robot    browser:${BROWSER}    feature:highlighting
Resource          ../../resources/Lab.robot
Resource          ../../resources/Browser.robot
Resource          ../../resources/Notebook.robot
Resource          ../../resources/LabRobot.robot
Resource          ../../resources/CodeMirror.robot
Resource          ../../resources/Elements.robot
Library           SeleniumLibrary
Library           OperatingSystem

*** Test Cases ***
Robot Syntax is Beautiful
    [Documentation]    Does CodeMirror syntax highlighting work as expected?
    [Template]    Robot Syntax Highlighting Should Yield Tokens
    basic${/}00_test_case
    # BEGIN RFUG
    rfug${/}2.1.3${/}in_the_space_separated_format_two__0
    rfug${/}2.1.3${/}one_file_can_contain_both_space__0
    # rfug${/}2.1.3${/}there_is_no_need_to_escape__0
    # rfug${/}2.1.4${/}empty_cells_can_be_escaped_either__0
    # rfug${/}2.1.4${/}all_the_syntax_discussed_above_is__0
    # rfug${/}2.1.4${/}all_the_syntax_discussed_above_is__1
    # rfug${/}2.2.1${/}the_second_column_normally_has_keyword__0
    # rfug${/}2.2.1${/}example_test_case_with_settings___0
    # rfug${/}2.2.2${/}the_test_below_uses_keywords_create__0
    # rfug${/}2.2.2${/}using_default_values_is_illustrated_by__0
    # rfug${/}2.2.2${/}for_example__remove_files_and_join__0
    # rfug${/}2.2.2${/}the_named_argument_syntax_requires_the__0
    # rfug${/}2.2.2${/}the_following_example_demonstrates_using_the__0
    # rfug${/}2.2.2${/}as_the_first_example_of_using__0
    # rfug${/}2.2.2${/}as_the_second_example__let_s_create__0
    # rfug${/}2.2.2${/}as_an_example_of_using_the__0
    # rfug${/}2.2.3${/}by_default_error_messages_are_normal__0
    # rfug${/}2.2.4${/}if_documentation_is_split_into_multiple__0
    # rfug${/}2.2.5${/}tags_are_free_text__but_they__0
    # rfug${/}2.2.6${/}the_easiest_way_to_specify_a__0
    # rfug${/}2.2.7${/}how_a_keyword_accepting_normal_positional__0
    # rfug${/}2.2.7${/}if_a_templated_test_case_has__0
    # rfug${/}2.2.7${/}templates_support_a_variation_of_the_embedded__0
    # rfug${/}2.2.7${/}when_embedded_arguments_are_used_with__0
    # rfug${/}2.2.7${/}if_templates_are_used_with_for__0
    # rfug${/}2.2.8${/}another_style_to_write_test_cases__0
    # rfug${/}2.2.8${/}the_above_example_has_six_separate__0
    # rfug${/}2.2.8${/}one_way_to_write_these_requirements_tests__0
    # rfug${/}2.3.1${/}tasks_are_created_based_on_the__0
    # rfug${/}2.4.2${/}the_main_usage_for_initialization_files__0
    # rfug${/}2.4.3${/}the_documentation_for_a_test_suite__0
    # rfug${/}2.4.4${/}the_name_and_value_for_the__0
    # rfug${/}2.5.1${/}in_those_cases_where_the_library__0
    # rfug${/}2.5.1${/}another_possibility_to_take_a_test__0
    # rfug${/}2.5.2${/}if_the_library_is_a_file___0
    # rfug${/}2.5.3${/}the_basic_syntax_for_specifying_the__0
    # rfug${/}2.5.3${/}possible_arguments_to_the_library_are__0
    # rfug${/}2.6.2${/}the_example_below_illustrates_the_usage__0
    # rfug${/}2.6.2${/}with_these_two_variables_set__we__0
    # rfug${/}2.6.2${/}when_a_variable_is_used_as__0
    # rfug${/}2.6.2${/}it_is_possible_to_use_list__0
    # rfug${/}2.6.2${/}list_variables_can_be_used_only__0
    # rfug${/}2.6.2${/}as_discussed_above__a_variable_containing__0
    # rfug${/}2.6.2${/}it_is_possible_to_use_dictionary__0
    # rfug${/}2.6.2${/}dictionary_variables_cannot_generally_be_used__0
    # rfug${/}2.6.2${/}it_is_possible_to_access_a__0
    # rfug${/}2.6.2${/}list_item_access_supports_also_the__0
    # rfug${/}2.6.2${/}if_a_key_is_a_string___0
    # rfug${/}2.6.2${/}also_nested_list_and_dictionary_structures__0
    # rfug${/}2.6.2${/}environment_variables_set_in_the_operating__0
    # rfug${/}2.6.2${/}when_running_tests_with_jython__it__0
    # rfug${/}2.6.3${/}the_simplest_possible_variable_assignment_is__0
    # rfug${/}2.6.3${/}it_is_also_possible__but_not__0
    # rfug${/}2.6.3${/}if_a_scalar_variable_has_a__0
    # rfug${/}2.6.3${/}creating_list_variables_is_as_easy__0
    # rfug${/}2.6.3${/}dictionary_variables_can_be_created_in__0
    # rfug${/}2.6.3${/}any_value_returned_by_a_keyword__0
    # rfug${/}2.6.3${/}notice_that_although_a_value_is__0
    # rfug${/}2.6.3${/}if_a_keyword_returns_a_list__0
    # rfug${/}2.6.3${/}if_a_keyword_returns_a_list__1
    # rfug${/}2.6.3${/}if_a_keyword_returns_a_dictionary__0
    # rfug${/}2.6.4${/}built_in_variables_related_to_the_operating__0
    # rfug${/}2.6.4${/}the_variable_syntax_can_be_used__0
    # rfug${/}2.6.4${/}it_is_possible_to_create_integers__0
    # rfug${/}2.6.4${/}also_boolean_values_and_python_none__0
    # rfug${/}2.6.4${/}it_is_possible_to_create_spaces__0
    # rfug${/}2.6.4${/}there_is_also_an_empty_list__0
    # rfug${/}2.6.6${/}the_most_common_usages_of_extended__0
    # rfug${/}2.6.6${/}many_standard_python_objects__including_strings__0
    # rfug${/}2.6.6${/}it_is_possible_to_set_attributes__0
    # rfug${/}2.6.6${/}in_the_example_below__do_x__0
    # rfug${/}2.7.1${/}in_many_ways__the_overall_user__0
    # rfug${/}2.7.2${/}user_keywords_can_have_a_documentation__0
    # rfug${/}2.7.3${/}starting_from_robot_framework_2_9__keywords__0
    # rfug${/}2.7.4${/}the_syntax_is_such_that_first__0
    # rfug${/}2.7.4${/}the_syntax_for_default_values_is__0
    # rfug${/}2.7.4${/}when_a_keyword_accepts_several_arguments__0
    # rfug${/}2.7.4${/}sometimes_even_default_values_are_not__0
    # rfug${/}2.7.4${/}the_keywords_in_the_examples_above__0
    # rfug${/}2.7.4${/}user_keywords_can_also_accept_free__0
    # rfug${/}2.7.4${/}starting_from_robot_framework_3_1__user__0
    # rfug${/}2.7.4${/}named_only_arguments_can_be_used_together__0
    # rfug${/}2.7.4${/}when_passing_named_only_arguments_to_keywords___0
    # rfug${/}2.7.4${/}named_only_arguments_can_have_default_values__0
    # rfug${/}2.7.5${/}it_has_always_been_possible_to__0
    # rfug${/}2.7.5${/}when_keywords_with_embedded_arguments_are__0
    # rfug${/}2.7.5${/}a_custom_embedded_argument_regular_expression__0
    # rfug${/}2.7.5${/}whenever_custom_embedded_argument_regular_expressions__0
    # rfug${/}2.7.5${/}the_biggest_benefit_of_having_arguments__0
    # rfug${/}2.7.6${/}user_keywords_can_also_return_several__0
    # rfug${/}2.7.6${/}the_first_example_below_is_functionally__0
    # rfug${/}2.7.7${/}keyword_teardown_works_much_in_the__0
    # rfug${/}2.8.1${/}resource_files_can_use_all_the__0
    # rfug${/}2.8.1${/}both_libdoc_and_ride_use_these__0
    # rfug${/}2.8.2${/}all_test_data_files_can_import__0
    # rfug${/}2.8.2${/}the_variables_in_both_the_examples__0
    # rfug${/}2.8.2${/}if_the_above_yaml_file_is__0
    # rfug${/}2.9.2${/}if_there_is_a_timeout__the__0
    # rfug${/}2.9.2${/}starting_from_robot_framework_3_0__timeout__0
    # rfug${/}2.9.3${/}the_keywords_used_in_the_for__0
    # rfug${/}2.9.3${/}it_is_often_convenient_to_use__0
    # rfug${/}2.9.3${/}for_loop_syntax_was_enhanced_in__0
    # rfug${/}2.9.3${/}having_nested_for_loops_is_not__0
    # rfug${/}2.9.3${/}if_there_are_lot_of_values__0
    # rfug${/}2.9.3${/}it_is_possible_to_use_simple__0
    # rfug${/}2.9.3${/}for_example__the_following_two_test__0
    # rfug${/}2.9.3${/}just_like_with_regular_for_loops___0
    # rfug${/}2.9.3${/}this_may_be_easiest_to_show__0
    # rfug${/}2.9.3${/}exit_for_loop_and_exit_for__0
    # rfug${/}2.9.3${/}continue_for_loop_and_continue_for__0
    # rfug${/}2.9.3${/}for_loops_can_be_excessive_in__0
    # rfug${/}4.1.2${/}the_number_of_arguments_needed_by__0
    # rfug${/}4.1.3${/}the_example_below_illustrates_how_the__0
    # rfug${/}4.1.3${/}it_is_possible_to_expose_a__0
    # rfug${/}4.1.3${/}the_first_example_keyword_above_can__0
    # rfug${/}4.1.3${/}python_supports_methods_accepting_any_number__0
    # rfug${/}4.1.3${/}if_you_are_already_familiar_how__0
    # rfug${/}4.1.3${/}the_following_example_illustrates_how_normal__0
    # rfug${/}4.1.3${/}starting_from_robot_framework_3_1__it__0
    # rfug${/}4.1.3${/}if_no_type_information_is_specified__0
    # rfug${/}4.1.3${/}the_coercion_works_with_the_numeric__0
    # rfug${/}4.1.3${/}library_keywords_can_also_accept_arguments__0
    # rfug${/}4.1.4${/}values_are_returned_using_the_return__0
    # rfug${/}4.1.4${/}keywords_can_also_return_values_so__0
    # rfug${/}4.1.6${/}using_the_named_argument_syntax_with__0
    # rfug${/}4.1.6${/}using_the_free_named_argument_syntax__0
    # rfug${/}4.1.6${/}using_the_named_only_argument_syntax_with__0
    # rfug${/}4.1.9${/}this_approach_is_clearly_better_than__0
    # rfug${/}4.2.2${/}the_remote_library_needs_to_know__0
    # rfug${/}5.1.2${/}possible_variables_in_resource_files_can__0
    # rfug${/}6.3.1${/}when_documenting_test_suites__test_cases__0
    # rfug${/}6.3.1${/}adding_newlines_manually_to_a_long__0
    # rfug${/}6.3.1${/}no_automatic_newline_is_added_if__0
    # rfug${/}6.3.2${/}for_example__the_following_test_suite__0
    # rfug${/}6.4.3${/}keyword_can_also_accept_other_special__0

    # END RFUG

*** Keywords ***
Robot Syntax Highlighting Should Yield Tokens
    [Arguments]    ${example}
    Run Keyword And Ignore Error    Click Element    css:.jp-Dialog-button.jp-mod-accept
    ${robot} =    Get File    ..${/}fixtures${/}highlighting${/}samples${/}${example}.robot
    Add a Cell    ${robot}
    ${observed} =    Get Cell Source Tokens
    ${cake} =    Evaluate    "\\n".join([" ".join(obs) for obs in ${observed}])
    Create File    ${OUTPUT DIR}${/}${BROWSER}${/}tokens${/}${example}.tokens    ${cake}
    ${raw} =    Get File    ..${/}fixtures${/}highlighting${/}tokens${/}${example}.tokens
    ${expected} =    Evaluate    [line.strip().split(" ") for line in """${raw}""".strip().split("\\n")]
    Should Be Equal    ${observed}    ${expected}

Make a Highlighting Notebook
    [Documentation]    Make a notebook for testing syntax highlighting
    Open JupyterLab with    ${BROWSER}
    Set Screenshot Directory    ${OUTPUT_DIR}${/}${BROWSER}${/}robot${/}highlighting
    Launch a new    Robot Framework    Notebook
