using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EasyWayToAddTssTerms
{
    public class TssTerm
    {
        public int Id { get; set; }
        public string TermName { get; set; }


        public static TssTerm FromRow(DataRow row)
        {
            TssTerm retTerm = new TssTerm();

            retTerm.Id = Convert.ToInt32(row["id"]);
            retTerm.TermName = Convert.ToString(row["term"]);

            return retTerm;
        }
    }
}
