using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UserControlLib;

namespace UserSentControl
{
    public class LoadedNewsEventargs : EventArgs
    {
        public FullInfoNewsAnalysis LoadedNews { get; set; }
    }


    public class LoadedListNewsEventargs : EventArgs
    {
        public List<News> LoadedNewsList { get; set; }
    }
}
