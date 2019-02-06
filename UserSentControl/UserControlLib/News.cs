using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserControlLib
{
    public class News
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string SubTitle { get; set; }
        public string FullText { get; set; }
        public string Link { get; set; }

        public DateTime NewsDate { get; set; }

        public static News FromRow(DataRow row)
        {

            try
            {
                News retNews = new News();

                retNews.Id = Convert.ToInt32(row["id"]);
                retNews.Title = Convert.ToString(row["title"]);
                retNews.SubTitle = Convert.ToString(row["subTitle"]);
                retNews.Link = Convert.ToString(row["link"]);
                if (row.Table.Columns.Contains("mainText"))
                    retNews.FullText = Convert.ToString(row["mainText"]);
                retNews.NewsDate = Convert.ToDateTime(row["newsDate"]);
                return retNews;
            }
            catch (Exception ex)
            {

            }
            return null;
        }
    }
}
