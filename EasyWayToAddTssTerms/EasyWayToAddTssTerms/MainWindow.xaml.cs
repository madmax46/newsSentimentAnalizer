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

namespace EasyWayToAddTssTerms
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        MainModel model;
        public MainWindow()
        {
            InitializeComponent();
            model = new MainModel();
        }
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            ReloadAllInfoFromBase();
        }

        private void ReloadAllInfoFromBase()
        {
            Task.Factory.StartNew(() =>
            {
                LoadAllTerms();
                LoadComboBoxes();
            });
        }

        private void LoadComboBoxes()
        {
            var instruments = model.LoadAllInstruments();
            var factors = model.LoadAllAffectingFactors();

            Dispatcher.Invoke(() =>
            {
                UIComboInstruments.ItemsSource = instruments;
                UIComboFactors.ItemsSource = factors;
            });
        }

        private void LoadAllTerms()
        {
            var terms = model.LoadAllTerms();
            Dispatcher.Invoke(() =>
            {
                UIAllTerms.ItemsSource = terms;
            });
        }

        private void UITerm_TextChanged(object sender, TextChangedEventArgs e)
        {

            TextBox senderBox = (TextBox)sender;
            if (string.IsNullOrEmpty(senderBox.Text))
                return;

            var finded = model.FindTermContainsSubsting(senderBox.Text);

            if (finded == null)
                return;

            UIAllTerms.SelectedItem = finded;
            UIAllTerms.ScrollIntoView(UIAllTerms.SelectedItem);
        }

        private void UIAddTerm_Click(object sender, RoutedEventArgs e)
        {
            var termTex = UITermNewText.Text;
            if (string.IsNullOrEmpty(termTex) || string.IsNullOrWhiteSpace(termTex))
                return;

            var selInstrument = (TssInstrument)UIComboInstruments.SelectedItem;

            if (selInstrument == null)
                return;

            var selFactor = (TssAffectingFactor)UIComboFactors.SelectedItem;

            if (selFactor == null)
                return;


            var res = model.AddNewTerm(selInstrument, selFactor, termTex);

            if (res == false)
                MessageBox.Show("Не удалось сохранить");

            LoadAllTerms();
        }

        private void UIChangeIp_Click(object sender, RoutedEventArgs e)
        {
            string ip = UIIp.Text;
            model.ChangeBaseIp(ip);
        }
    }
}
