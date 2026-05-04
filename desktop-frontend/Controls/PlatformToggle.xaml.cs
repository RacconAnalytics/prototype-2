using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;

namespace desktop_frontend.Controls
{
    public partial class PlatformToggle : UserControl
    {
        public event Action<bool>? OnPlatformChanged;

        private bool isYouTube = true;
        private const double SegmentWidth = 160;
        private const double AnimationDuration = 0.35;

        public PlatformToggle()
        {
            InitializeComponent();
            UpdateColors();
        }

        private void YouTubeRadio_Checked(object sender, RoutedEventArgs e)
        {
            if (!isYouTube)
            {
                isYouTube = true;
                AnimateToPosition(0);
                UpdateColors();
                OnPlatformChanged?.Invoke(true);
            }
        }

        private void TrendsRadio_Checked(object sender, RoutedEventArgs e)
        {
            if (isYouTube)
            {
                isYouTube = false;
                AnimateToPosition(1);
                UpdateColors();
                OnPlatformChanged?.Invoke(false);
            }
        }

        private void AnimateToPosition(int position)
        {
            double targetOffset = position * SegmentWidth;

            var animation = new DoubleAnimation
            {
                To = targetOffset,
                Duration = TimeSpan.FromSeconds(AnimationDuration),
                EasingFunction = new CubicEase { EasingMode = EasingMode.EaseOut }
            };

            PillTranslate.BeginAnimation(TranslateTransform.XProperty, animation);
        }

        private void UpdateColors()
        {
            if (isYouTube)
            {
                PillBackground.Color = Color.FromRgb(255, 0, 0);
            }
            else
            {
                PillBackground.Color = Colors.White;
            }
        }

        public void SetPlatform(bool isYouTube)
        {
            this.isYouTube = isYouTube;
            if (isYouTube)
                YouTubeRadio.IsChecked = true;
            else
                TrendsRadio.IsChecked = true;
            
            Canvas.SetLeft(PillIndicator, isYouTube ? 0 : SegmentWidth);
            UpdateColors();
        }
    }
}