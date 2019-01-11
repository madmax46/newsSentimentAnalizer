using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EasyWayToAddTssTerms
{
    public class TssAffectingFactor
    {
        public int Id { get; set; }

        public string Name { get; set; }


        public static TssAffectingFactor FromRow(DataRow row)
        {
            TssAffectingFactor retFactor = new TssAffectingFactor();

            retFactor.Id = Convert.ToInt32(row["id"]);
            retFactor.Name = Convert.ToString(row["name"]);

            return retFactor;
        }
    }
}
