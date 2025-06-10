import flet as ft

def main(page: ft.Page):
    # Page settings
    page.title = "Modern Auth"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#10162c", "#0c2749", "#0f0f23", "#1a1a2e"],
            tile_mode=ft.GradientTileMode.MIRROR
        )
    )
    page.scroll = ft.ScrollMode.HIDDEN
    page.theme = ft.Theme(scrollbar_theme=ft.ScrollbarTheme(thickness=0.0))
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.safe_area = True
    page.notch_shape = ft.NotchShape.AUTO

    # Enhanced Colors & Styles
    PRIMARY_COLOR = "#4f46e5"       # Deep indigo for primary actions
    PLACEHOLDER_COLOR = "#9ca3af"   # Softer neutral for hint text
    FIELD_BG = "#1f2937"            # Dark slate for input fields
    BORDER_COLOR = "#374151"        # Neutral border with good contrast
    TEXT_COLOR = "#f3f4f6"          # Near-white for clarity
    ERROR_COLOR = "#f87171"         # Softer red for errors
    SUCCESS_COLOR = "#34d399"       # Minty green for success
    BUTTON_RADIUS = 12              # Slightly smaller for a sharper modern look
    FORM_WIDTH = 380

    # Form state
    form_type = "sign_in"

    # Refs
    username_ref = ft.Ref[ft.TextField]()
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    confirm_password_ref = ft.Ref[ft.TextField]()
    form_container_ref = ft.Ref[ft.Container]()

    # Error message Text control
    error_text = ft.Text("", color=ERROR_COLOR, size=13, visible=False, weight=ft.FontWeight.W_500)

    def validate_email(email):
        return "@" in email and "." in email.split("@")[-1]

    def clear_fields():
        """Clear all form fields"""
        if username_ref.current:
            username_ref.current.value = ""
        if email_ref.current:
            email_ref.current.value = ""
        if password_ref.current:
            password_ref.current.value = ""
        if confirm_password_ref.current:
            confirm_password_ref.current.value = ""

    def switch_form(e, to_form):
        nonlocal form_type
        form_type = to_form
        error_text.value = ""
        error_text.visible = False
        clear_fields()
        update_content()

    def show_banner(message: str, is_success: bool = True):
        color = SUCCESS_COLOR if is_success else ERROR_COLOR
        icon = ft.Icons.CHECK_CIRCLE if is_success else ft.Icons.ERROR
        
        page.banner = ft.Banner(
            bgcolor=color,
            leading=ft.Icon(icon, color=ft.Colors.WHITE, size=24),
            content=ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
            actions=[
                ft.TextButton(
                    "OK", 
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        overlay_color=ft.Colors.WHITE12
                    ),
                    on_click=lambda e: setattr(page.banner, 'open', False) or page.update()
                )
            ]
        )
        page.banner.open = True
        page.update()

    def on_sign_in(e):
        email = email_ref.current.value.strip() if email_ref.current.value else ""
        password = password_ref.current.value.strip() if password_ref.current.value else ""
        
        if not email or not password:
            error_text.value = "Please fill in all fields"
            error_text.visible = True
        elif not validate_email(email):
            error_text.value = "Please enter a valid email address"
            error_text.visible = True
        else:
            error_text.visible = False
            show_banner("Welcome back! Login successful.", True)
        page.update()

    def on_sign_up(e):
        username = username_ref.current.value.strip() if username_ref.current.value else ""
        email = email_ref.current.value.strip() if email_ref.current.value else ""
        password = password_ref.current.value.strip() if password_ref.current.value else ""
        confirm_password = confirm_password_ref.current.value.strip() if confirm_password_ref.current.value else ""
        
        if not username or not email or not password or not confirm_password:
            error_text.value = "Please fill in all fields"
            error_text.visible = True
        elif len(username) < 3:
            error_text.value = "Username must be at least 3 characters"
            error_text.visible = True
        elif not validate_email(email):
            error_text.value = "Please enter a valid email address"
            error_text.visible = True
        elif len(password) < 6:
            error_text.value = "Password must be at least 6 characters"
            error_text.visible = True
        elif password != confirm_password:
            error_text.value = "Passwords do not match"
            error_text.visible = True
        else:
            error_text.visible = False
            show_banner("Account created successfully! You can now sign in.", True)
            switch_form(None, "sign_in")
        page.update()

    def social_button(text, icon, icon_color):
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(icon, color=icon_color, size=20),
                        ft.Text(text, color=TEXT_COLOR, weight=ft.FontWeight.W_500)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                width=FORM_WIDTH,
                height=48,
                style=ft.ButtonStyle(
                    bgcolor=PRIMARY_COLOR,
                    color=TEXT_COLOR,
                    elevation=0,
                    surface_tint_color=ft.Colors.TRANSPARENT,
                    overlay_color=ft.Colors.WHITE12,
                    side=ft.BorderSide(width=1, color=BORDER_COLOR),
                    shape=ft.RoundedRectangleBorder(radius=BUTTON_RADIUS),
                ),
            ),
            border_radius=BUTTON_RADIUS,
        )

    def create_text_field(ref, label, icon, password=False):
        return ft.TextField(
            ref=ref,
            label=label,
            prefix_icon=icon,
            password=password,
            can_reveal_password=password,
            border_radius=BUTTON_RADIUS,
            filled=True,
            cursor_color=PRIMARY_COLOR,
            fill_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            border_color=BORDER_COLOR,
            focused_border_color=PRIMARY_COLOR,
            label_style=ft.TextStyle(color=PLACEHOLDER_COLOR, size=14),
            text_style=ft.TextStyle(color=TEXT_COLOR, size=15),
            width=FORM_WIDTH,
            height=56,
        )

    def build_form():
        # Header section
        header = ft.Column([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.SECURITY_ROUNDED if form_type == "sign_in" else ft.Icons.PERSON_ADD_ROUNDED,
                    size=64,
                    color=PRIMARY_COLOR
                ),
                width=120,
                height=120,
                border_radius=60,
                alignment=ft.alignment.center
            ),
            ft.Text(
                "Welcome Back" if form_type == "sign_in" else "Create Account",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=TEXT_COLOR,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Sign in to continue" if form_type == "sign_in" else "Join us today",
                size=16,
                color=PLACEHOLDER_COLOR,
                text_align=ft.TextAlign.CENTER
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)

        # Form fields
        fields = []
        
        if form_type == "sign_up":
            fields.append(create_text_field(username_ref, "Username", ft.Icons.PERSON_OUTLINED))
        
        fields.extend([
            create_text_field(email_ref, "Email Address", ft.Icons.EMAIL_OUTLINED),
            create_text_field(password_ref, "Password", ft.Icons.LOCK_OUTLINED, password=True)
        ])
        
        if form_type == "sign_up":
            fields.append(create_text_field(confirm_password_ref, "Confirm Password", ft.Icons.LOCK_OUTLINED, password=True))

        # Main action button
        main_button = ft.Container(
            content=ft.ElevatedButton(
                text="Sign In" if form_type == "sign_in" else "Create Account",
                width=FORM_WIDTH,
                bgcolor=PRIMARY_COLOR,
                height=52,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                    shape=ft.RoundedRectangleBorder(radius=BUTTON_RADIUS),
                    elevation=4,
                    shadow_color=f"{PRIMARY_COLOR}40"
                ),
                on_click=on_sign_in if form_type == "sign_in" else on_sign_up,
            ),
            border_radius=BUTTON_RADIUS,
        )

        # Footer section
        footer_text = "Don't have an account?" if form_type == "sign_in" else "Already have an account?"
        footer_button_text = "Sign Up" if form_type == "sign_in" else "Sign In"
        footer_action = lambda e: switch_form(e, "sign_up" if form_type == "sign_in" else "sign_in")

        footer = ft.Column([
            ft.TextButton(
                text="Forgot Password?" if form_type == "sign_in" else None,
                style=ft.ButtonStyle(color=PRIMARY_COLOR),
                visible=form_type == "sign_in"
            ),
            ft.Row([
                ft.Text(footer_text, color=PLACEHOLDER_COLOR, size=14),
                ft.TextButton(
                    text=footer_button_text,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        overlay_color=f"{PRIMARY_COLOR}20"
                    ),
                    on_click=footer_action,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Text("Or continue with", color=PLACEHOLDER_COLOR, size=14),
            social_button("Continue with Google", ft.Icons.ANDROID, ft.Colors.GREEN),
            social_button("Continue with Apple", ft.Icons.APPLE, ft.Colors.WHITE),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)

        return ft.Column([
            header,
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            *fields,
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            error_text,
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            main_button,
            footer
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16)

    # Main container with enhanced styling
    main_container = ft.SafeArea(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    ref=form_container_ref,
                    content=build_form(),
                    padding=0
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            padding=ft.padding.only(top=0, left=20, right=20, bottom=0),
        )
    )

    def update_content():
        """Update the form content when switching between sign-in and sign-up"""
        form_container_ref.current.content = build_form()
        page.update()

    # Initial render
    page.add(main_container)

if __name__ == "__main__":
    ft.app(target=main)