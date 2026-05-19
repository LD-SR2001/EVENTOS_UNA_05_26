from models.event import Event
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository
from views.console_view import ConsoleView


def _auth_loop(view: ConsoleView, user_ctrl: UserController) -> bool:
    """Executa o loop de autenticacao. Retorna False se o usuario quiser sair."""
    while not user_ctrl.current_user:
        choice = view.show_welcome_menu()

        if choice == '0':
            return False

        elif choice == '1':
            cpf = view.get_login_input()
            user = user_ctrl.login(cpf)
            if not user:
                view.show_message(
                    "CPF nao encontrado. Verifique ou crie uma conta.",
                    success=False,
                )

        elif choice == '2':
            data = view.get_register_input()
            if not all(data.values()):
                view.show_message("Preencha todos os campos.", success=False)
                continue
            user = user_ctrl.register(**data)
            if not user:
                view.show_message("CPF ja cadastrado. Faca login.", success=False)
            else:
                view.show_message(f"Conta criada! Bem-vindo(a), {user.name}!")

    return True


def _handle_event_detail(view: ConsoleView, event_ctrl: EventController,
                         user_ctrl: UserController, event: Event) -> None:
    user = user_ctrl.current_user
    is_confirmed = event.id in user.confirmed_events
    action = view.show_event_detail(event, user, is_confirmed)

    if action != '1':
        return

    if is_confirmed:
        if view.confirm_action("Cancelar sua participacao neste evento?"):
            event_ctrl.cancel_participation(event, user)
            user_ctrl.save_current_user()
            view.show_message("Participacao cancelada.")
    else:
        if event.is_past():
            view.show_message("Este evento ja encerrou.", success=False)
            return
        if view.confirm_action(f"Confirmar participacao em '{event.name}'?"):
            event_ctrl.confirm_participation(event, user)
            user_ctrl.save_current_user()
            view.show_message(f"Presenca confirmada em '{event.name}'!")


def _main_loop(view: ConsoleView, event_ctrl: EventController,
               user_ctrl: UserController) -> str:
    """Executa o loop principal. Retorna 'exit' ou 'logout'."""
    while True:
        user = user_ctrl.current_user
        choice = view.show_main_menu(user)

        if choice == '0':
            return 'exit'

        elif choice == '1':
            events = event_ctrl.get_upcoming_events()
            selected = view.show_event_list(events, "PROXIMOS EVENTOS", user)
            if selected:
                _handle_event_detail(view, event_ctrl, user_ctrl, selected)

        elif choice == '2':
            events = event_ctrl.get_happening_now()
            selected = view.show_event_list(
                events, "EVENTOS EM ANDAMENTO AGORA", user
            )
            if selected:
                _handle_event_detail(view, event_ctrl, user_ctrl, selected)

        elif choice == '3':
            events = event_ctrl.get_past_events()
            selected = view.show_event_list(events, "EVENTOS PASSADOS", user)
            if selected:
                _handle_event_detail(view, event_ctrl, user_ctrl, selected)

        elif choice == '4':
            data = view.get_event_input()
            if data:
                event = Event(
                    name=data['name'],
                    address=data['address'],
                    category=data['category'],
                    event_datetime=data['datetime'],
                    description=data['description'],
                    duration_hours=data['duration'],
                )
                event_ctrl.add_event(event)
                view.show_message(f"Evento '{event.name}' cadastrado com sucesso!")

        elif choice == '5':
            my_events = event_ctrl.get_user_events(user)
            action, selected = view.show_my_events(my_events, user)
            if action == 'select' and selected:
                _handle_event_detail(view, event_ctrl, user_ctrl, selected)

        elif choice == '6':
            user_ctrl.logout()
            return 'logout'


def main() -> None:
    view = ConsoleView()
    event_ctrl = EventController(EventRepository())
    user_ctrl = UserController(UserRepository())

    while True:
        authenticated = _auth_loop(view, user_ctrl)
        if not authenticated:
            break

        result = _main_loop(view, event_ctrl, user_ctrl)
        if result == 'exit':
            break


if __name__ == '__main__':
    main()
