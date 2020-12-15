import instances
import my_plotly
import webbrowser
import my_SQL

if __name__ == "__main__":
    state = input('Enter a state name (e.g. Michigan, michigan) or "exit"\n:').lower()
    state_dict = instances.build_state_url_dict()
    
    my_SQL.build_state_table()
    my_SQL.build_college_table()
        
    jud=True
    
    while jud:
        
        if state == 'exit':
            exit()
        
        elif state not in state_dict.keys():
            print('[Error] Enter proper state name')
            print('\n----------------------------------')
            state = input('Enter a state name (e.g. Michigan, michigan) or "exit"\n:').lower()
            jud=True

        
        elif state in state_dict.keys():
            my_SQL.insert_college(state)
            instance_list = instances.get_sites_for_state(state_dict[state])
            print('----------------------------------')
            print(f'List of colleges in {state}')
            print('----------------------------------')

            for i in range(0,len(instance_list)):
                if i != '':
                    print('[' + str(i+1) +'] '+instance_list[i].info())
                else:
                    pass
            jud=False
            
            
            further_search = input('''\nYou can check "tuition" ,"enrollment" or "deatils". \nYou can also choose the number for detail search or "exit" or "back" :\n''').lower()
            jud_2=True
            
            while jud_2:
                
                if further_search == 'exit':
                    exit()
                elif further_search == 'back':
                    state = input('\nEnter a state name (e.g. Michigan, michigan) or "exit"\n:').lower()
                    jud_2=False
                    jud=True
                elif further_search=='':
                    print('[Error] Invalid input')
                    print('\n----------------------------------')
                    further_search = input('\nYou can check "tuition" ,"enrollment" or "deatils". \nYou can also choose the number for detail search or "exit" or "back" :\n').lower()
                    jud_2 = True   

                elif further_search == 'tuition':  
                    my_plotly.compare_tuition(state_dict[state],state.capitalize())
                    further_search = input('\nYou can check "tuition" ,"enrollment" or "deatils". \nYou can also choose the number for detail search or "exit" or "back" :\n').lower()
                    jud_2 = True

                elif further_search == 'details':  
                    my_plotly.show_college_info(state_dict[state],state.capitalize())
                    further_search = input('\nYou can check "tuition" ,"enrollment" or "deatils". \nYou can also choose the number for detail search or "exit" or "back" :\n').lower()
                    jud_2 = True

                elif further_search == 'enrollment' :
                    my_plotly.compare_enrollment(state_dict[state],state.capitalize())
                    further_search = input('\nYou can check "tuition" ,"enrollment" or "deatils". \nYou can also choose the number for detail search or "exit" or "back" :\n').lower()
                    jud_2 = True
                
                elif further_search.isnumeric()==True and int(further_search) >= 1 and int(further_search) <= len(instance_list):
                    
                    college_instance=instance_list[int(further_search)-1]
                    print(f'\nYou choose {college_instance.name}.')


                    input_3=input('Do you want to look at this college in browser? Y/N\n').lower()

                    if input_3=='y':
                        webbrowser.open(college_instance.url)
                    elif input_3=='n':
                        pass
                    else:
                        print('[Error] Invalid input, back to college list.')
                        print('\n----------------------------------')


                    
                    input_4=input('Do you want to search this college in map and find near places? Y/N\n').lower()

                    if input_4=='y':
                        my_plotly.show_map_info(college_instance)
                        webbrowser.open(f'https://www.mapquest.com/search/results?query={college_instance.city}')
                                        
                    
                    elif input_3=='n':
                        pass
                    else:
                        print('[Error] Invalid input, back to college list.')
                        print('\n----------------------------------')

                                        
                    
                    further_search = input('Choose the number for detail search or "exit" or "back"\n:').lower()
                    jud_2 = True    
                    
                
                else:
                    print('[Error] Invalid input')
                    print('\n----------------------------------')
                    further_search = input('\nYou can check "tuition" ,"enrollment" or "deatils". \nYou can also choose the number for detail search or "exit" or "back" :\n').lower()
                    jud_2 = True