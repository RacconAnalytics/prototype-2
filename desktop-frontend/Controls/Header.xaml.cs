using System;
using System.Windows;
using System.Windows.Controls;

namespace desktop_frontend.Controls
{
    public partial class Header : UserControl
    {
        public event Action? OnLoginClicked;
        public event Action? OnRegisterClicked;
        public event Action? OnHomeClicked;

        public Header()
        {
            InitializeComponent();
        }

        private void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            OnLoginClicked?.Invoke();
        }

        private void RegisterButton_Click(object sender, RoutedEventArgs e)
        {
            OnRegisterClicked?.Invoke();
        }

        private void TextButton_Click(object sender, RoutedEventArgs e)
        {
            OnHomeClicked?.Invoke();
        }
    }
}