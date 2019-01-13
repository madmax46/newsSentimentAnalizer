using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EasyWayToAddTssTerms
{
    public class MainModel
    {
        IDBProvider dBProvider;

        List<TssTerm> allTerms = new List<TssTerm>();
        List<TssInstrument> allInstruments = new List<TssInstrument>();
        List<TssAffectingFactor> allAffectingFactors = new List<TssAffectingFactor>();
        DataTable fullInfoByTerms = new DataTable();
        int findedFullInfoByTermsIndex = -1;
        public MainModel()
        {
            MySQLConfig config = new MySQLConfig()
            {
                Host = "localhost",
                Port = 3306,
                UserId = "root",
                Password = "28Q{f6NA!r",
                SslMode = "none",
                Database = "stockthesaurus",
                CharacterSet = "cp1251"
            };
            dBProvider = new MySQLWrap(config);
        }

        public List<TssTerm> LoadAllTerms()
        {
            string query = "SELECT id,term FROM stockthesaurus.tss_terms";
            var dt = GetDataTableByQuery(query);

            if (dt == null)
                return new List<TssTerm>();

            List<TssTerm> retValues = new List<TssTerm>();
            foreach (DataRow oneRow in dt.Rows)
            {
                retValues.Add(TssTerm.FromRow(oneRow));
            }
            allTerms = retValues;
            return retValues;
        }


        public TssTerm FindTermContainsSubsting(string substing)
        {
            TssTerm retTerm = null;
            int indexStartWith = int.MaxValue;
            foreach (var oneTerm in allTerms)
            {
                var tempIndex = oneTerm.TermName.IndexOf(substing, StringComparison.CurrentCultureIgnoreCase);
                if (tempIndex != -1)
                {
                    if (tempIndex < indexStartWith)
                    {
                        indexStartWith = tempIndex;
                        retTerm = oneTerm;
                    }
                }
            }
            return retTerm;
        }

        public int FindIdRowTermContainsSubstingInAllInfo(string substing, bool isFindNext = false)
        {
            int lastFindedIndex = findedFullInfoByTermsIndex;

            findedFullInfoByTermsIndex = -1;

            if (fullInfoByTerms == null || fullInfoByTerms.Rows.Count == 0 || !fullInfoByTerms.Columns.Contains("term"))
                return findedFullInfoByTermsIndex;

            int index = 0;
            List<int> idxFinded = new List<int>();
            foreach (DataRow oneInfo in fullInfoByTerms.Rows)
            {
                var termText = Convert.ToString(oneInfo["term"]);
                var tempIndex = termText.IndexOf(substing, StringComparison.CurrentCultureIgnoreCase);
                if (tempIndex != -1)
                {
                    idxFinded.Add(index);
                }
                index++;
            }

            if (!idxFinded.Any())
                return findedFullInfoByTermsIndex;

            if (isFindNext == false || idxFinded.Max() == lastFindedIndex)
                return findedFullInfoByTermsIndex = idxFinded.First();

            foreach (int oneIndex in idxFinded)
            {
                if (oneIndex > lastFindedIndex)
                {
                    findedFullInfoByTermsIndex = oneIndex;
                    break;
                }
            }

            return findedFullInfoByTermsIndex;
        }


        public DataTable ShowFullInfoByTerms()
        {
            try
            {
                var res = dBProvider.ProcedureByName("ShowFullInfoByTerms");
                fullInfoByTerms = res;
            }
            catch (Exception ex)
            {
                fullInfoByTerms = new DataTable();
            }
            return fullInfoByTerms;
        }



        public List<TssInstrument> LoadAllInstruments()
        {

            string query = "SELECT id,name FROM stockthesaurus.tss_instruments";
            var dt = GetDataTableByQuery(query);

            if (dt == null)
                return new List<TssInstrument>();

            List<TssInstrument> retValues = new List<TssInstrument>();
            foreach (DataRow oneRow in dt.Rows)
            {
                retValues.Add(TssInstrument.FromRow(oneRow));
            }
            allInstruments = retValues;
            return retValues;
        }

        public bool AddNewTerm(TssInstrument selInstrument, TssAffectingFactor selFactor, string termTex)
        {
            bool retStatus = false;
            try
            {
                termTex = termTex.Trim();
                var res = dBProvider.ProcedureByName("AddTermToReletion", selInstrument.Id, selFactor.Id, MySQLWrap.ToMySqlParamStat(termTex));
                if (res.Rows.Count != 0)
                {
                    if (Convert.ToString(res.Rows[0]["res"]) == "yes")
                        retStatus = true;
                }
            }
            catch (Exception ex)
            {

            }

            return retStatus;
        }

        public void ChangeBaseIp(string host)
        {
            if (host.Count(r => r == '.') != 3 && host != "localhost")
                return;

            var config = ((MySQLWrap)dBProvider).ConnectConfig;
            config.Host = host;
            ((MySQLWrap)dBProvider).ChangeConfig(config);
        }

        public List<TssAffectingFactor> LoadAllAffectingFactors()
        {
            string query = "SELECT id, name FROM stockthesaurus.tss_factors";
            var dt = GetDataTableByQuery(query);

            if (dt == null)
                return new List<TssAffectingFactor>();

            List<TssAffectingFactor> retValues = new List<TssAffectingFactor>();
            foreach (DataRow oneRow in dt.Rows)
            {
                retValues.Add(TssAffectingFactor.FromRow(oneRow));
            }
            allAffectingFactors = retValues;
            return retValues;
        }




        private DataTable GetDataTableByQuery(string query)
        {
            try
            {
                var dt = dBProvider.GetDataTable(query);
                return dt;
            }
            catch (Exception ex)
            {
                return null;
            }
        }
    }
}
