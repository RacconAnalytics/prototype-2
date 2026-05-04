using System.Windows;
using desktop_frontend.Views;

namespace desktop_frontend;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        MainHeader.OnLoginClicked += () => MainFrame.Navigate(new SignInPage());
        MainHeader.OnRegisterClicked += () => MainFrame.Navigate(new CreateAccountPage());
        MainHeader.OnHomeClicked += () => MainFrame.Navigate(new HomePage());
        MainFrame.Navigate(new HomePage());
    }
}