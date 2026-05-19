import os
from datetime import datetime
from models.event import Event
from models.user import User
from models.category import Category


def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def _pause():
    input("\n  Pressione ENTER para continuar...")


def _divider(width: int = 52) -> str:
    return "  " + "-" * width


HEADER = """
+======================================================+
|         SISTEMA DE EVENTOS DA CIDADE                 |
+======================================================+"""


class ConsoleView:

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _header(self, user: User = None) -> None:
        _clear()
        print(HEADER)
        if user:
            print(f"  Logado como: {user.name}  |  Cidade: {user.city}")
        print()

    def _event_status_label(self, event: Event) -> str:
        if event.is_happening_now():
            return "[EM ANDAMENTO AGORA]"
        if event.is_past():
            return "[ENCERRADO]"
        delta = event.datetime - datetime.now()
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"[Em {days}d {hours}h]"
        if hours > 0:
            return f"[Em {hours}h]"
        minutes = delta.seconds // 60
        return f"[Em {minutes} min]"

    # ------------------------------------------------------------------ #
    #  Auth screens                                                        #
    # ------------------------------------------------------------------ #

    def show_welcome_menu(self) -> str:
        self._header()
        print("  1. Entrar (login por CPF)")
        print("  2. Criar conta")
        print("  0. Sair")
        print()
        return input("  Opcao: ").strip()

    def get_login_input(self) -> str:
        self._header()
        print("  LOGIN")
        print(_divider(40))
        print()
        return input("  CPF: ").strip()

    def get_register_input(self) -> dict:
        self._header()
        print("  CADASTRO DE USUARIO")
        print(_divider(40))
        print()
        name = input("  Nome completo : ").strip()
        email = input("  E-mail        : ").strip()
        cpf = input("  CPF           : ").strip()
        phone = input("  Telefone      : ").strip()
        city = input("  Cidade        : ").strip()
        return {'name': name, 'email': email, 'cpf': cpf,
                'phone': phone, 'city': city}

    # ------------------------------------------------------------------ #
    #  Main menu                                                           #
    # ------------------------------------------------------------------ #

    def show_main_menu(self, user: User) -> str:
        self._header(user)
        print("  -- EVENTOS ------------------------------------------")
        print("  1. Proximos eventos")
        print("  2. Eventos em andamento agora")
        print("  3. Eventos passados")
        print("  4. Cadastrar novo evento")
        print()
        print("  -- MINHA PARTICIPACAO --------------------------------")
        print("  5. Meus eventos confirmados")
        print()
        print("  -- CONTA ---------------------------------------------")
        print("  6. Trocar de conta (logout)")
        print("  0. Encerrar programa")
        print()
        return input("  Opcao: ").strip()

    # ------------------------------------------------------------------ #
    #  Event list                                                          #
    # ------------------------------------------------------------------ #

    def show_event_list(self, events: list, title: str,
                        user: User = None):
        self._header(user)
        print(f"  {title}")
        print(_divider())

        if not events:
            print("  Nenhum evento encontrado.")
            _pause()
            return None

        for i, event in enumerate(events, 1):
            status = self._event_status_label(event)
            print(f"  {i:2}. {event.name}  {status}")
            print(f"      {event.category.value}  |  "
                  f"{event.datetime.strftime('%d/%m/%Y %H:%M')}")
            print(f"      {event.address}")
            print()

        print("  0. Voltar")
        print()
        choice = input("  Selecione um evento para ver detalhes (0 = voltar): ").strip()

        if choice == '0':
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(events):
                return events[idx]
        except ValueError:
            pass

        return None

    # ------------------------------------------------------------------ #
    #  Event detail                                                        #
    # ------------------------------------------------------------------ #

    def show_event_detail(self, event: Event, user: User,
                          is_confirmed: bool) -> str:
        self._header(user)
        status = self._event_status_label(event)

        print(f"  Nome      : {event.name}")
        print(f"  Status    : {status}")
        print(f"  Categoria : {event.category.value}")
        print(f"  Data/Hora : {event.datetime.strftime('%d/%m/%Y as %H:%M')}")
        print(f"  Termino   : {event.end_datetime.strftime('%d/%m/%Y as %H:%M')}")
        print(f"  Endereco  : {event.address}")
        print(f"  Inscritos : {len(event.participants)} pessoa(s)")
        print()
        print(f"  Descricao:")
        print(f"  {event.description}")
        print()
        print(_divider())

        if not event.is_past():
            if is_confirmed:
                print("  1. Cancelar minha participacao")
            else:
                print("  1. Confirmar minha participacao")

        print("  0. Voltar")
        print()
        return input("  Opcao: ").strip()

    # ------------------------------------------------------------------ #
    #  My events                                                           #
    # ------------------------------------------------------------------ #

    def show_my_events(self, events: list, user: User):
        self._header(user)
        print("  MEUS EVENTOS CONFIRMADOS")
        print(_divider())

        if not events:
            print("  Voce nao confirmou participacao em nenhum evento.")
            _pause()
            return 'back', None

        upcoming = [e for e in events if not e.is_past()]
        past = [e for e in events if e.is_past()]
        all_shown = []

        if upcoming:
            print("  Proximos / Em andamento:")
            for event in upcoming:
                all_shown.append(event)
                status = self._event_status_label(event)
                print(f"  {len(all_shown):2}. {event.name}  {status}")
                print(f"      {event.datetime.strftime('%d/%m/%Y %H:%M')}  |  {event.address}")
                print()

        if past:
            print("  Ja ocorreram:")
            for event in past:
                all_shown.append(event)
                print(f"  {len(all_shown):2}. {event.name}  [ENCERRADO]")
                print(f"      {event.datetime.strftime('%d/%m/%Y %H:%M')}")
                print()

        print("  0. Voltar")
        print()
        choice = input("  Selecione um evento (0 = voltar): ").strip()

        if choice == '0':
            return 'back', None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_shown):
                return 'select', all_shown[idx]
        except ValueError:
            pass

        return 'back', None

    # ------------------------------------------------------------------ #
    #  Event registration form                                             #
    # ------------------------------------------------------------------ #

    def get_event_input(self):
        self._header()
        print("  CADASTRAR NOVO EVENTO")
        print(_divider(40))
        print()

        name = input("  Nome do evento: ").strip()
        if not name:
            return None

        address = input("  Endereco      : ").strip()
        description = input("  Descricao     : ").strip()

        print()
        print("  Categorias disponiveis:")
        categories = list(Category)
        for i, cat in enumerate(categories, 1):
            print(f"  {i:2}. {cat.value}")
        print()

        category = None
        while category is None:
            try:
                choice = int(input("  Escolha a categoria: "))
                if 1 <= choice <= len(categories):
                    category = categories[choice - 1]
                else:
                    print("  Opcao fora do intervalo.")
            except ValueError:
                print("  Digite um numero valido.")

        print()
        event_datetime = None
        while event_datetime is None:
            try:
                date_str = input("  Data do evento (DD/MM/AAAA): ").strip()
                time_str = input("  Hora de inicio (HH:MM)     : ").strip()
                event_datetime = datetime.strptime(
                    f"{date_str} {time_str}", "%d/%m/%Y %H:%M"
                )
            except ValueError:
                print("  Formato invalido. Tente novamente.")

        duration = None
        while duration is None:
            try:
                val = float(input("  Duracao (horas, ex: 2.5)   : ").strip())
                if val > 0:
                    duration = val
                else:
                    print("  A duracao deve ser maior que zero.")
            except ValueError:
                print("  Valor invalido.")

        return {
            'name': name,
            'address': address,
            'description': description,
            'category': category,
            'datetime': event_datetime,
            'duration': duration,
        }

    # ------------------------------------------------------------------ #
    #  Feedback messages                                                   #
    # ------------------------------------------------------------------ #

    def show_message(self, message: str, success: bool = True) -> None:
        prefix = "[OK]" if success else "[ERRO]"
        print(f"\n  {prefix} {message}")
        _pause()

    def confirm_action(self, message: str) -> bool:
        answer = input(f"\n  {message} (s/n): ").strip().lower()
        return answer == 's'
