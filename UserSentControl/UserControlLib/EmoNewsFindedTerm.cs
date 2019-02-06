using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserControlLib
{
    public class EmoNewsFindedTerm
    {
        public int Id { get; set; }

        public int IdNews { get; set; }
        public int IdEmoTerm { get; set; }
        public int StartInText { get; set; }
        public int StopInText { get; set; }


        public static EmoNewsFindedTerm FromRow(DataRow row)
        {
            try
            {
                EmoNewsFindedTerm retEmoNewsFindedTerm = new EmoNewsFindedTerm();

                retEmoNewsFindedTerm.IdNews = Convert.ToInt32(row["id"]);
                retEmoNewsFindedTerm.IdNews = Convert.ToInt32(row["idNews"]);
                retEmoNewsFindedTerm.IdEmoTerm = Convert.ToInt32(row["idEmoTerm"]);
                retEmoNewsFindedTerm.StartInText = Convert.ToInt32(row["start"]);
                retEmoNewsFindedTerm.StopInText = Convert.ToInt32(row["stop"]);
                return retEmoNewsFindedTerm;
            }
            catch (Exception ex)
            {

            }
            return null;
        }


    }
}
