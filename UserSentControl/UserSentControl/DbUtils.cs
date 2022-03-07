using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserSentControl
{
    public static class DBUtils
    {
        private static object SyncRoot = new object();
        private static MySQLWrap myWrap;
        public static MySQLWrap MyWrap
        {
            get
            {
                if (myWrap == null)
                {
                    lock (SyncRoot)
                    {
                        if (myWrap == null)
                        {
                            MySQLConfig config = new MySQLConfig()
                            {
                                Host = "localhost",
                                Port = 3306,
                                UserId = "root",
                                SslMode = "none",
                                CharacterSet = "cp1251"
                            };
                            myWrap = new MySQLWrap(config);
                        }
                    }
                }

                return myWrap;
            }
        }

        private static object SyncRootUniver = new object();
        private static MySQLWrap myWrapUniver;
        public static MySQLWrap MyWrapUniver
        {
            get
            {
                if (myWrapUniver == null)
                {
                    lock (SyncRootUniver)
                    {
                        if (myWrapUniver == null)
                        {
                            MySQLConfig config = new MySQLConfig()
                            {
                            };
                            myWrapUniver = new MySQLWrap(config);
                        }
                    }
                }

                return myWrapUniver;
            }
        }

    }
}

