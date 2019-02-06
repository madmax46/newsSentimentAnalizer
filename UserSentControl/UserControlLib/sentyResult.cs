using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserControlLib
{
    public class SentyResult
    {
        public int IdNews { get; set; }
        public float PositiveValue { get; set; }
        public float NegativeValue { get; set; }
        public float NeutralValue { get; set; }
        public float ResEval { get; set; }


        public static SentyResult FromRow(DataRow row)
        {
            try
            {
                SentyResult retSentyResult = new SentyResult();

                retSentyResult.IdNews = Convert.ToInt32(row["idNews"]);
                retSentyResult.PositiveValue = Convert.ToSingle(row["positiveValue"]);
                retSentyResult.NegativeValue = Convert.ToSingle(row["negativeValue"]);
                retSentyResult.NeutralValue = Convert.ToSingle(row["neutralValue"]);
                retSentyResult.ResEval = Convert.ToSingle(row["resEval"]);
                return retSentyResult;
            }
            catch (Exception ex)
            {

            }
            return null;
        }

    }
}
