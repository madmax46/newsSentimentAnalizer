using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using UserControlLib;

namespace UserSentControl
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        MainModel m_model = null;
        public MainWindow()
        {
            InitializeComponent();
            m_model = new MainModel();
            m_model.LoadedAnalyzedNews += M_model_LoadedNews;
            m_model.ErrorThrown += M_model_ErrorThrown;
            m_model.LoadedNewsList += M_model_LoadedNewsList; ;

        }

        private void M_model_LoadedNewsList(object sender, LoadedListNewsEventargs e)
        {
            Dispatcher.Invoke(() =>
            {
                UINewsList.ItemsSource = e.LoadedNewsList;
            });

        }

        private void M_model_ErrorThrown(object sender, Exception e)
        {
            Dispatcher.Invoke(() =>
            {
                ShowMsg(e.ToString());
            });
        }

        private static void ShowMsg(string msg)
        {
            MessageBox.Show(msg);
        }

        private void M_model_LoadedNews(object sender, LoadedNewsEventargs e)
        {


            Dispatcher.Invoke(() =>
            {
                UIFullNewsText.Document.Blocks.Clear();
                UIFullNewsText.Document.Blocks.Add(new Paragraph(new Run(e.LoadedNews.NewsText.FullText)));

                foreach (var oneSelect in e.LoadedNews.EmoFindedTerms)
                {
                    var termScore = e.LoadedNews.EmoDict.FirstOrDefault(r => r.Id == oneSelect.IdEmoTerm)?.Score;
                    if (termScore == null)
                        continue;

                    SolidColorBrush brush = Brushes.Yellow;
                    if (termScore >= 1)
                        brush = Brushes.Green;
                    if (termScore <= -1)
                        brush = Brushes.Red;

                    ApplyColor(UIFullNewsText, oneSelect.StartInText, oneSelect.StopInText, brush);
                }

                UINewsDate.Text = Convert.ToString(e.LoadedNews.NewsText.NewsDate);
                UITitle.Text = Convert.ToString(e.LoadedNews.NewsText.Title);
                UISubTitle.Text = Convert.ToString(e.LoadedNews.NewsText.SubTitle);

                UIFindedTermsGrid.ItemsSource = e.LoadedNews.EmoDict;
                UIEvaluation.ItemsSource = new List<SentyResult>() { e.LoadedNews.SentyNewsResult };
                UIFindedCount.Text = Convert.ToString(e.LoadedNews.EmoFindedTerms.Count);
                UITabControl.SelectedIndex = 1;
                Cursor = Cursors.Arrow;
            });

        }

        private void UIUpdateNewsButton_Click(object sender, RoutedEventArgs e)
        {
            m_model.ReLoadLastNews();

        }


        private void ApplyColor(RichTextBox richTextBox, int startposition, int endposition, Brush color)
        {

            var flowDocument = richTextBox.Document;
            TextPointer start = FindPointerAtTextOffset(
                    flowDocument.ContentStart, startposition, seekStart: true);
            if (start == null)
            {
                // позиция вне документа, выходим
                return;
            }

            TextPointer end = FindPointerAtTextOffset(
                    start, endposition - startposition, seekStart: false);
            if (end == null)
            {
                // позиция вне документа, выходим
                return;
            }

            richTextBox.Selection.Select(start, end);
            richTextBox.Selection.ApplyPropertyValue(TextElement.BackgroundProperty, color);
        }


        TextPointer FindPointerAtTextOffset(TextPointer from, int offset, bool seekStart)
        {
            if (from == null)
                return null;

            TextPointer current = from;
            TextPointer end = from.DocumentEnd;
            int charsToGo = offset;

            while (current.CompareTo(end) != 0)
            {
                Run currentRun;
                if (current.GetPointerContext(LogicalDirection.Forward) == TextPointerContext.Text &&
                    (currentRun = current.Parent as Run) != null)
                {
                    var remainingLengthInRun = current.GetOffsetToPosition(currentRun.ContentEnd);
                    if (charsToGo < remainingLengthInRun ||
                        (charsToGo == remainingLengthInRun && !seekStart))
                        return current.GetPositionAtOffset(charsToGo);
                    charsToGo -= remainingLengthInRun;
                    current = currentRun.ElementEnd;
                }
                else
                {
                    current = current.GetNextContextPosition(LogicalDirection.Forward);
                }
            }
            if (charsToGo == 0 && !seekStart)
                return end;
            return null;
        }

        private void UINewsLink_Click(object sender, RoutedEventArgs e)
        {
            m_model.OpenCurrentLink();
        }

        private void UIFindNews_Click(object sender, RoutedEventArgs e)
        {
            m_model.LoadListOfNews(UILimitNews.Text, UINewsId.Text, UIOffset.Text);
        }

        private void Row_DoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (UINewsList.SelectedItem == null)
            {
                ShowMsg("Не выделен элемент");
                return;
            }

            var selectedNews = (News)UINewsList.SelectedItem;
            if (selectedNews == null)
            {
                ShowMsg("Не выделен элемент");
                return;
            }
            LoadNews(selectedNews.Id);
        }

        private void LoadNews(int idNews)
        {
            Cursor = Cursors.Wait;
            m_model.LoadNews(idNews);
            //UITabControl =
            //UITabControl.
        }
    }
}
