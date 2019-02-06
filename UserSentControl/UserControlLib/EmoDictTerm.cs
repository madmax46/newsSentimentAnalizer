using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserControlLib
{
    public class EmoDictTerm
    {
        public EmoDictTerm()
        {
            TermLemmas = new string[0];
        }

        public int Id { get; set; }
        public string Term { get; set; }
        public float Score { get; set; }
        public string TermLemma { get; set; }
        public string[] TermLemmas { get; set; }



        public static EmoDictTerm FromRow(DataRow row)
        {
            try
            {
                EmoDictTerm retEmoNewsFindedTerm = new EmoDictTerm();

                retEmoNewsFindedTerm.Id = Convert.ToInt32(row["id"]);
                retEmoNewsFindedTerm.Term = Convert.ToString(row["term"]);
                retEmoNewsFindedTerm.TermLemma = Convert.ToString(row["termLemma"]);
                retEmoNewsFindedTerm.Score = Convert.ToSingle(row["value"]);
                retEmoNewsFindedTerm.TermLemmas = retEmoNewsFindedTerm.TermLemma.Split(' ');
                return retEmoNewsFindedTerm;
            }
            catch (Exception ex)
            {

            }
            return null;
        }

    }
}
