from quiz_game import QuizGame

def main():
    game = QuizGame()
    game.load_state()

    while True:
        choice = game.show_menu()
        
        if choice == '1':
            game.play_quiz()
        elif choice == '2':
            game.add_quiz()
        elif choice == '3':
            game.list_quizzes()
        elif choice == '4':
            game.show_best_score()
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 번호입니다. 다시 선택해주세요.")

if __name__ == '__main__':
    main()
