from quiz_game import QuizGame


def main():
    game = QuizGame()
    game.load_state()

    try:
        while True:
            choice = game.show_menu()

            if choice == 1:
                game.play_quiz()
            elif choice == 2:
                game.add_quiz()
            elif choice == 3:
                game.list_quizzes()
            elif choice == 4:
                game.show_best_score()
            elif choice == 5:
                print("프로그램을 종료합니다.")
                game.save_state()
                break
    except (KeyboardInterrupt, EOFError):
        print("입력이 중단되어 안전하게 종료합니다.")
        game.save_state()

if __name__ == '__main__':
    main()
