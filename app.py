if __name__ == '__main__':
    while True :
        print('''
            What do you want to do ? 
            1. Update Data
            2. Update Sentiment Value
            3. Fetch Data
            4. Visualize 
            5. Exit
            
        ''')
        option = input('input the number\n')
        if option == '1' : 
            from loot_data import load_data
            load_data()
    
        elif option == '2' :
            from update_data import update_sentiment
            update_sentiment()
            
        elif option == '3' :
            from show_data import fetch_data
            fetch_data()
            
        elif option == '4' :
            from visualize import visualize_data 
            visualize_data()
            
        else : 
            exit()
    

