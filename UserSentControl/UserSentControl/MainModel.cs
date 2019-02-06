using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UserControlLib;

namespace UserSentControl
{
    public class MainModel
    {

        public event EventHandler<LoadedNewsEventargs> LoadedAnalyzedNews;
        public event EventHandler<Exception> ErrorThrown;

        public event EventHandler<LoadedListNewsEventargs> LoadedNewsList;


        private static FullInfoNewsAnalysis fullInfoNewsAnalysis { get; set; }

        private int lastLoadedId { get; set; }
        public void LoadNews(int idNews)
        {
            //double dig = 1123 / 14;
            lastLoadedId = idNews;
            Task.Factory.StartNew(() =>
            {
                LoadNewsFromDb(idNews);
            });
        }
        public void ReLoadLastNews()
        {
            LoadNews(lastLoadedId);
        }


        private void LoadNewsFromDb(int idNews)
        {
            string procName = $"stockthesaurus.GetFullNewsAnalysisInfo";
            var ds = GetDataSetFromDb(DBUtils.MyWrap, procName, idNews);

            if (ds.Tables.Count == 0)
                return;

            if (ds.Tables[0].Rows.Count == 0)
                return;

            var fullInfo = FullInfoNewsAnalysis.FromDS(ds);

            fullInfoNewsAnalysis = fullInfo;
            LoadedAnalyzedNews?.Invoke(this, new LoadedNewsEventargs() { LoadedNews = fullInfo });
        }


        private DataTable GetDataTableFromDb(IDBProvider db, string query)
        {
            int iter = 0;
            while (iter++ < 3)
            {
                try
                {
                    var res = db.GetDataTable(query);
                    return res;
                }
                catch (Exception ex)
                {

                }
            }
            return new DataTable();
        }

        private DataTable GetDataTableByProcedure(IDBProvider db, string ProcedureDSByName, params object[] par)
        {
            int iter = 0;
            while (iter++ < 3)
            {
                try
                {
                    var res = db.ProcedureByName(ProcedureDSByName, par);
                    return res;
                }
                catch (Exception ex)
                {

                }
            }
            return new DataTable();
        }

        private DataSet GetDataSetFromDb(IDBProvider db, string ProcedureDSByName, params object[] par)
        {
            int iter = 0;
            while (iter++ < 3)
            {
                try
                {
                    var res = db.ProcedureDSByName(ProcedureDSByName, par);
                    return res;
                }
                catch (Exception ex)
                {

                }
            }
            return new DataSet();
        }

        public void OpenCurrentLink()
        {
            Task.Factory.StartNew(() =>
            {
                if (fullInfoNewsAnalysis?.NewsText?.Link == null)
                    return;

                string url = string.Concat("https://tass.ru", fullInfoNewsAnalysis?.NewsText?.Link);

                System.Diagnostics.Process.Start(url);
            });
        }

        public void LoadListOfNews(string limitStr, string idNewsStr, string offsetStr)
        {
            Task.Factory.StartNew(() =>
            {
                try
                {
                    int limit = 0;
                    int? idNews = null;
                    int offset = 0;
                    int idNewsNoNull = 0;

                    if (!string.IsNullOrEmpty(limitStr))
                        int.TryParse(limitStr, out limit);

                    if (!string.IsNullOrEmpty(idNewsStr))
                        if (int.TryParse(idNewsStr, out idNewsNoNull))
                            idNews = idNewsNoNull;

                    if (!string.IsNullOrEmpty(offsetStr))
                        offset = int.Parse(offsetStr);

                    LoadNewsListFromDb(limit, idNews, offset);
                }
                catch (Exception ex)
                {

                }
            });

        }

        private void LoadNewsListFromDb(int? limit, int? idNews, int? offset)
        {
            string procName = $"stockthesaurus.Cl_GetAnalisedNews";

            var db = GetDataTableByProcedure(DBUtils.MyWrap, procName, limit, idNews, offset);

            if (db.Rows.Count == 0)
                return;

            List<News> listNews = new List<News>();
            foreach (DataRow oneRow in db.Rows)
            {
                var fullInfo = News.FromRow(oneRow);
                if (fullInfo == null)
                    continue;

                listNews.Add(fullInfo);
            }

            LoadedNewsList?.Invoke(this, new LoadedListNewsEventargs() { LoadedNewsList = listNews });



            //stockthesaurus.Cl_GetAnalisedNews(IN inLimit INT, IN inNewsId INT, IN inOffset INT)

        }
    }
}
