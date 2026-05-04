using System.Windows;
using System.Windows.Controls;
using MaterialDesignThemes.Wpf;

namespace desktop_frontend.Views
{
    public partial class SignInPage : Page
    {
        private bool isPasswordVisible = false;
        private bool isSyncingPassword = false;

        public SignInPage()
        {
            InitializeComponent();
        }

        private void PasswordBox_PasswordChanged(object sender, RoutedEventArgs e)
        {
            if (isSyncingPassword) return;
            isSyncingPassword = true;
            PasswordTextBox.Text = PasswordBox.Password;
            isSyncingPassword = false;
        }

        private void PasswordTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (isSyncingPassword) return;
            isSyncingPassword = true;
            PasswordBox.Password = PasswordTextBox.Text;
            isSyncingPassword = false;
        }

        private void TogglePassword_Click(object sender, RoutedEventArgs e)
        {
            isPasswordVisible = !isPasswordVisible;
            if (isPasswordVisible)
            {
                PasswordTextBox.Text = PasswordBox.Password;
                PasswordBox.Visibility = Visibility.Collapsed;
                PasswordTextBox.Visibility = Visibility.Visible;
                PasswordEyeIcon.Kind = PackIconKind.EyeOff;
            }
            else
            {
                PasswordBox.Password = PasswordTextBox.Text;
                PasswordBox.Visibility = Visibility.Visible;
                PasswordTextBox.Visibility = Visibility.Collapsed;
                PasswordEyeIcon.Kind = PackIconKind.Eye;
            }
        }

        private void SignUpLink_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.Navigate(new CreateAccountPage());
        }
    }
}