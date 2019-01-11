using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EasyWayToAddTssTerms
{
    public class TssInstrument
    {
        public int Id { get; set; }

        public string Name { get; set; }


        public static TssInstrument FromRow(DataRow row)
        {
            TssInstrument retInstrument = new TssInstrument();

            retInstrument.Id = Convert.ToInt32(row["id"]);
            retInstrument.Name = Convert.ToString(row["name"]);

            return retInstrument;
        }
    }
}
