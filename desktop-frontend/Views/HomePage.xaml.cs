using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace desktop_frontend.Views
{
    public partial class HomePage : Page
    {
        private bool isYouTube = true;

        private readonly LinearGradientBrush googleGradientBrush = new LinearGradientBrush
        {
            StartPoint = new Point(0, 0.5),
            EndPoint = new Point(1, 0.5),
            GradientStops = new GradientStopCollection
            {
                new GradientStop(Colors.Blue, 0),
                new GradientStop(Colors.Green, 0.2),
                new GradientStop(Colors.Yellow, 0.4),
                new GradientStop(Colors.Orange, 0.6),
                new GradientStop(Colors.Red, 0.8),
                new GradientStop(Colors.Purple, 1)
            }
        };

        public HomePage()
        {
            InitializeComponent();
            PlatformToggleControl.OnPlatformChanged += OnPlatformToggleChanged;
            UpdatePlatformUI();
        }

        private void OnPlatformToggleChanged(bool isYouTube)
        {
            this.isYouTube = isYouTube;
            UpdatePlatformUI();
        }

        private void UpdatePlatformUI()
        {
            if (LogoBackground == null || YouTubeIcon == null || GoogleTrendsIcon == null || 
                TitleText == null || SubtitleText == null || SearchButton == null || VideoSelectorPanel == null)
                return;

            if (isYouTube)
            {
                LogoBackground.Background = new SolidColorBrush(Color.FromRgb(255, 0, 0));
                YouTubeIcon.Visibility = Visibility.Visible;
                GoogleTrendsIcon.Visibility = Visibility.Collapsed;
                TitleText.Text = "Buscador de YouTube";
                SubtitleText.Text = "Descubre si está en tendencia en YouTube";
                SearchButton.Background = new SolidColorBrush(Color.FromRgb(255, 0, 0));
                VideoSelectorPanel.Visibility = Visibility.Visible;
            }
            else
            {
                LogoBackground.Background = new SolidColorBrush(Colors.White);
                YouTubeIcon.Visibility = Visibility.Collapsed;
                GoogleTrendsIcon.Visibility = Visibility.Visible;
                TitleText.Text = "Buscador de Google Trends";
                SubtitleText.Text = "Descubre si está en tendencia en Google Trends";
                SearchButton.Background = googleGradientBrush;
                VideoSelectorPanel.Visibility = Visibility.Collapsed;
            }
        }

        private void SearchButton_Click(object sender, RoutedEventArgs e)
        {
            // Frontend only - no backend yet
        }
    }
}