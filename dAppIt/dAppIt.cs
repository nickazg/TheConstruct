using Neo.SmartContract.Framework;
using Neo.SmartContract.Framework.Services.Neo;
using Neo.SmartContract.Framework.Services.System;
using System;
using System.Numerics;

namespace dAppIt
{
    public class dAppItContract : Neo.SmartContract.Framework.SmartContract
    {
        public static byte[] contract_creator = new byte[0];
        public static byte[] contract_admin = new byte[0];
        public static char[] separating_char = {'$'};
        
        public static Object Main(string operation, params object[] args)
        {
            Runtime.Notify("Version 0.1");

            // Contract transaction, ie assest deposit/withdrawl transaction (operation == signature)
            if (Runtime.Trigger == TriggerType.Verification)
            {
                return false;
            }

            // Invocation transaction
            else if (Runtime.Trigger == TriggerType.Application)
            {

            }
            return false;
        }

        // USER METHODS

        // Saves username with user_hash as key.
        private static bool RegisterNewUser(byte[] user_hash, string username)
        {
            // If invoker isnt user_hash
            if (!Runtime.CheckWitness(user_hash)) return false;

            string user_hash_string = user_hash.AsString();

            // If user_hash doesnt exist
            if (Storage.Get(Storage.CurrentContext, user_hash_string).Length == 0)
            {
                Storage.Put(Storage.CurrentContext, user_hash_string, username);

                // Add user_hash to global array of users
                StoragePutToStringArray("contract_users", user_hash_string);
                return true;
            }

            return false;
                        
        }

        private static bool EditUser()
        {
            return true;
        }

        private static bool RemoveUser()
        {
            return true;
        }
        // USER METHODS - END


        // PROJECT METHODS
        private static bool RegisterNewProject()
        {
            return true;
        }

        private static bool EditProject()
        {
            return true;
        }

        private static bool RemoveProject()
        {
            return true;
        }
        // PROJECT METHODS - END


        // CONTRACT METHODS
        private static bool RegisterNewContract()
        {
            return true;
        }

        private static bool EditContract()
        {
            return true;
        }

        private static bool RemoveContract()
        {
            return true;
        }
        // CONTRACT METHODS - END


        // UTILITY METHODS
        private static string[] StorageGetStringArray(string key)
        {
            // Get raw stored string (converted from raw byte[])
            string key_storage = Storage.Get(Storage.CurrentContext, key).AsString();

            // Convert string to string[], split by the separating_char
            string[] key_storage_array = key_storage.Split(separating_char);

            return key_storage_array;
        }

        private static void StoragePutToStringArray(string key, string value)
        {
            // Gets stored string[] from key
            string[] key_storage_array = StorageGetStringArray(key);

            // Converts string[] back to a string separated by the "separating_char"
            string key_storage_string = String.Join(separating_char.ToString(), key_storage_array);

            // Adding new value to string
            key_storage_string = string.Concat(key_storage_string, string.Concat(separating_char.ToString(), value));

            // Puts the string to storage
            Storage.Put(Storage.CurrentContext, key, key_storage_string);
        }
        // UTILITY METHODS - END


    }
}
