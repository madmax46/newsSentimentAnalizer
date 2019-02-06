using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserControlLib
{
    public class FullInfoNewsAnalysis
    {
        public FullInfoNewsAnalysis()
        {
            EmoFindedTerms = new List<EmoNewsFindedTerm>();
            EmoDict = new List<EmoDictTerm>();
        }

        public News NewsText { get; set; }
        public SentyResult SentyNewsResult { get; set; }
        public List<EmoNewsFindedTerm> EmoFindedTerms { get; set; }
        public List<EmoDictTerm> EmoDict { get; set; }


        public static FullInfoNewsAnalysis FromDS(DataSet dataSet)
        {
            try
            {
                FullInfoNewsAnalysis fullInfoNewsAnalysis = new FullInfoNewsAnalysis();
                var news = News.FromRow(dataSet.Tables[0].Rows[0]);
                SentyResult emoRes = null;
                if (dataSet.Tables[1].Rows.Count > 0)
                    emoRes = SentyResult.FromRow(dataSet.Tables[1].Rows[0]);
                List<EmoNewsFindedTerm> emoFindedTerms = new List<EmoNewsFindedTerm>();
                foreach (DataRow oneRow in dataSet.Tables[2].Rows)
                {
                    var oneFindedTerm = EmoNewsFindedTerm.FromRow(oneRow);
                    if (oneFindedTerm != null)
                        emoFindedTerms.Add(oneFindedTerm);
                }


                List<EmoDictTerm> emoDictTerms = new List<EmoDictTerm>();
                foreach (DataRow oneRow in dataSet.Tables[3].Rows)
                {
                    var oneDictTerm = EmoDictTerm.FromRow(oneRow);
                    if (oneDictTerm != null)
                        emoDictTerms.Add(oneDictTerm);
                }

                fullInfoNewsAnalysis.NewsText = news;
                fullInfoNewsAnalysis.SentyNewsResult = emoRes;
                fullInfoNewsAnalysis.EmoFindedTerms = emoFindedTerms;
                fullInfoNewsAnalysis.EmoDict = emoDictTerms;

                return fullInfoNewsAnalysis;
            }
            catch (Exception ex)
            {

            }
            return new FullInfoNewsAnalysis();
        }
    }
}
