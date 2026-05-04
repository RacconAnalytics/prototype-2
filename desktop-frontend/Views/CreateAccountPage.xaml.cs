using System.Windows;
using System.Windows.Controls;
using MaterialDesignThemes.Wpf;

namespace desktop_frontend.Views
{
    public partial class CreateAccountPage : Page
    {
        private bool isPasswordVisible = false;
        private bool isConfirmPasswordVisible = false;
        private bool isSyncingPassword = false;
        private bool isSyncingConfirmPassword = false;

        public CreateAccountPage()
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

        private void ConfirmPasswordBox_PasswordChanged(object sender, RoutedEventArgs e)
        {
            if (isSyncingConfirmPassword) return;
            isSyncingConfirmPassword = true;
            ConfirmPasswordTextBox.Text = ConfirmPasswordBox.Password;
            isSyncingConfirmPassword = false;
        }

        private void ConfirmPasswordTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (isSyncingConfirmPassword) return;
            isSyncingConfirmPassword = true;
            ConfirmPasswordBox.Password = ConfirmPasswordTextBox.Text;
            isSyncingConfirmPassword = false;
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

        private void ToggleConfirmPassword_Click(object sender, RoutedEventArgs e)
        {
            isConfirmPasswordVisible = !isConfirmPasswordVisible;
            if (isConfirmPasswordVisible)
            {
                ConfirmPasswordTextBox.Text = ConfirmPasswordBox.Password;
                ConfirmPasswordBox.Visibility = Visibility.Collapsed;
                ConfirmPasswordTextBox.Visibility = Visibility.Visible;
                ConfirmPasswordEyeIcon.Kind = PackIconKind.EyeOff;
            }
            else
            {
                ConfirmPasswordBox.Password = ConfirmPasswordTextBox.Text;
                ConfirmPasswordBox.Visibility = Visibility.Visible;
                ConfirmPasswordTextBox.Visibility = Visibility.Collapsed;
                ConfirmPasswordEyeIcon.Kind = PackIconKind.Eye;
            }
        }

        private void SignInLink_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.Navigate(new SignInPage());
        }
    }
}