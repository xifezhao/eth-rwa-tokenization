from web3 import Web3
import json
import time
import pandas as pd
import os # For file existence check
from decimal import Decimal, getcontext # For precise calculations

# --- Configuration ---
GANACHE_URL = "http://127.0.0.1:8545"  # Ensure this matches your Ganache setup
ETH_PRICE_USD = 2000  # Assumed ETH price (USD)
L2_GAS_EFFICIENCY_FACTOR = 0.1  # Simulated L2 internal gas efficiency vs L1
L2_FIXED_TX_FEE_ETH = 0.00001 # Simplified L2 base transaction fee (ETH, simulated)
L1_BATCH_SUBMISSION_BASE_GAS = 21000 + 20000 # Base L1 tx gas + simulated data storage gas per batch
L1_GAS_PRICE_GWEI = 20 # Assumed L1 Gas Price (Gwei) - will be overridden by Ganache's actual price in script
MOCK_ORACLE_SERVICE_FEE_USD = 0.1 # Assumed Oracle service fee (USD)

# --- Connect to Ganache ---
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    print(f"Error: Could not connect to Ganache ({GANACHE_URL})!")
    print("Please ensure Ganache is running and the URL/port are correct.")
    exit()

try:
    if not w3.eth.accounts:
        print("Error: No accounts available in Ganache. Check Ganache configuration.")
        exit()
    w3.eth.default_account = w3.eth.accounts[0] # Use the first account as default
    deployer = w3.eth.accounts[0]
    user1 = w3.eth.accounts[1] if len(w3.eth.accounts) > 1 else deployer # Ensure account exists
    user2 = w3.eth.accounts[2] if len(w3.eth.accounts) > 2 else deployer # Ensure account exists
    print(f"Successfully connected to Ganache. Default Account (Deployer): {deployer}")
except Exception as e:
    print(f"Error connecting to Ganache or getting accounts: {e}")
    exit()


# --- Helper: Load compiled contract ABI and Bytecode ---
def load_compiled_contract(contract_name):
    build_path_relative = f'./build/contracts/{contract_name}.json'
    script_cwd = os.getcwd()
    absolute_build_path = os.path.abspath(os.path.join(script_cwd, build_path_relative))

    print(f"  Loading compiled {contract_name} from (expected absolute path): {absolute_build_path}...")

    if not os.path.exists(absolute_build_path):
        error_message = (
            f"Error: Compiled contract file not found: {absolute_build_path}\n"
            "Ensure:\n"
            "1. 'truffle compile' was run in the Truffle project root (e.g., 'experiment_4').\n"
            "2. 'truffle compile' executed successfully without errors.\n"
            "3. This Python script is run from the Truffle project root.\n"
            f"   Current script CWD: {script_cwd}\n"
        )
        print(error_message)
        raise FileNotFoundError(error_message)
    try:
        with open(absolute_build_path) as f:
            contract_json = json.load(f)
            abi = contract_json['abi']
            bytecode = contract_json.get('bytecode', contract_json.get('deployedBytecode'))
            if not bytecode:
                raise ValueError(f"Bytecode not found in {contract_name}.json")
        return abi, bytecode
    except KeyError as e:
        error_message = f"Error: Missing expected key in {contract_name}.json: {e}"
        print(error_message)
        raise KeyError(error_message)
    except json.JSONDecodeError:
        error_message = f"Error: Could not parse {contract_name}.json ({absolute_build_path}). Not valid JSON."
        print(error_message)
        raise json.JSONDecodeError(error_message, "", 0)
    except Exception as e:
        error_message = f"Unknown error loading contract {contract_name}: {e}"
        print(error_message)
        raise Exception(error_message)

# --- Helper: Deploy contract ---
def deploy_contract(abi, bytecode, *args):
    ContractFactory = w3.eth.contract(abi=abi, bytecode=bytecode)
    contract_name_for_error = "UnknownContract" # ABI has no direct contract name

    try:
        print(f"    Attempting to deploy contract (args: {args})...")
        tx_params_deploy = {'from': deployer}
        
        tx_hash = ContractFactory.constructor(*args).transact(tx_params_deploy)
        print(f"      Deployment tx sent, Hash: {tx_hash.hex()}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)

        if tx_receipt.status == 0:
            print(f"!! Contract {contract_name_for_error} deployment failed (tx reverted):")
            print(f"   Receipt: {tx_receipt}")
            raise Exception(f"Contract {contract_name_for_error} deployment failed, tx reverted (status 0)")

        contract_instance = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        print(f"    Contract {contract_name_for_error} (actual type may vary) deployed at: {contract_instance.address}")
        return contract_instance
    except Exception as e:
        print(f"!! Critical error deploying contract {contract_name_for_error}: {e}")
        if hasattr(e, 'message') and e.message: print(f"  Details: {e.message}")
        if hasattr(e, 'args') and e.args and isinstance(e.args[0], dict) and 'message' in e.args[0]:
            print(f"  Potential Revert Message: {e.args[0]['message']}")
        elif 'revert' in str(e).lower() or 'execution reverted' in str(e).lower():
            print("  This looks like a contract revert. Check constructor args, contract logic, and Ganache logs.")
        raise


# --- Helper: Execute L1 transaction and get cost ---
def execute_l1_transaction(contract_function_call, account, value_eth=0):
    function_name = contract_function_call.fn_name if hasattr(contract_function_call, 'fn_name') else 'Unknown Function'
    try:
        tx_params = {'from': account}
        if value_eth > 0:
            tx_params['value'] = w3.to_wei(value_eth, 'ether')

        tx_hash = contract_function_call.transact(tx_params)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt.status == 0:
            print(f"!! L1 transaction ({function_name}) failed (tx reverted):")
            print(f"   Receipt: {receipt}")
            return None, None, None, receipt

        gas_used = receipt.gasUsed
        try:
            actual_gas_price = w3.eth.get_transaction(tx_hash).gasPrice
        except: # Fallback if tx not found immediately (should be rare with wait_for_transaction_receipt)
            actual_gas_price = w3.to_wei(L1_GAS_PRICE_GWEI, 'gwei')

        tx_cost_eth_decimal = w3.from_wei(gas_used * actual_gas_price, 'ether') # Web3.py returns Decimal
        tx_cost_usd = float(tx_cost_eth_decimal) * ETH_PRICE_USD
        return gas_used, float(tx_cost_eth_decimal), tx_cost_usd, receipt
    except Exception as e:
        print(f"!! L1 transaction ({function_name}) failed: {e}")
        if hasattr(e, 'message') and e.message: print(f"  Details: {e.message}")
        if hasattr(e, 'args') and e.args and isinstance(e.args[0], dict) and 'message' in e.args[0]:
            print(f"  Potential Revert Message: {e.args[0]['message']}")
        return None, None, None, None


# --- Simulate L2 transaction cost calculation ---
def calculate_l2_tx_cost(l1_equivalent_gas_used, batch_size, l1_gas_price_gwei_val):
    l1_gas_price_wei = w3.to_wei(l1_gas_price_gwei_val, 'gwei')
    l2_internal_gas_simulated = Decimal(str(l1_equivalent_gas_used)) * Decimal(str(L2_GAS_EFFICIENCY_FACTOR))

    # Cost of L2 internal operations (simulated)
    l2_op_gas_price_simulated_wei = Decimal(str(l1_gas_price_wei)) * Decimal('0.1') # Assume L2 gas price is 10% of L1
    l2_internal_op_cost_wei = l2_internal_gas_simulated * l2_op_gas_price_simulated_wei
    
    l2_fixed_tx_fee_decimal = Decimal(str(L2_FIXED_TX_FEE_ETH))
    internal_op_cost_eth_decimal = w3.from_wei(int(l2_internal_op_cost_wei.to_integral_value()), 'ether') # Convert to int for from_wei
    
    l2_tx_fee_eth_simulated_decimal = l2_fixed_tx_fee_decimal + internal_op_cost_eth_decimal

    # Cost of L1 batch submission (amortized)
    l1_data_gas_per_tx_in_batch = Decimal('200') # Simulated gas per tx for L1 data
    l1_batch_submission_base_gas_decimal = Decimal(str(L1_BATCH_SUBMISSION_BASE_GAS))

    l1_batch_submission_gas_total = l1_batch_submission_base_gas_decimal + (l1_data_gas_per_tx_in_batch * Decimal(str(batch_size)))
    amortized_l1_gas_per_l2_tx = l1_batch_submission_gas_total / Decimal(str(batch_size))
    
    amortized_l1_cost_eth_decimal = w3.from_wei(int(amortized_l1_gas_per_l2_tx.to_integral_value() * l1_gas_price_wei), 'ether')

    total_l2_tx_cost_eth_decimal = l2_tx_fee_eth_simulated_decimal + amortized_l1_cost_eth_decimal
    
    total_l2_tx_cost_eth_float = float(total_l2_tx_cost_eth_decimal)
    total_l2_tx_cost_usd = total_l2_tx_cost_eth_float * ETH_PRICE_USD
    
    return float(l2_internal_gas_simulated), total_l2_tx_cost_eth_float, total_l2_tx_cost_usd

# --- Main experiment logic ---
def run_experiment():
    print(f"Python script CWD: {os.getcwd()}")
    test_json_path_relative = './build/contracts/MyERC20Token.json' # For path check
    print(f"Target MyERC20Token.json (from {os.getcwd()} finding {test_json_path_relative}) exists: {os.path.exists(test_json_path_relative)}")

    results = []
    num_runs_per_tx_type = 1 # For faster debugging, set to 1 initially
    l2_batch_sizes_to_test = [10, 50]

    erc20_token = None
    erc721_token = None
    rwa_manager = None
    simple_dao = None
    mock_oracle = None

    try:
        print("\n--- Loading compiled contracts ---")
        erc20_abi, erc20_bytecode = load_compiled_contract('MyERC20Token')
        erc721_abi, erc721_bytecode = load_compiled_contract('MyERC721Token')
        rwa_manager_abi, rwa_manager_bytecode = load_compiled_contract('RWAManager')
        dao_abi, dao_bytecode = load_compiled_contract('SimpleDAO')
        oracle_abi, oracle_bytecode = load_compiled_contract('MockOracle')

        print("\n--- Deploying contracts to Ganache ---")
        initial_supply_erc20 = 1000000 * (10**18)

        print("  Deploying MyERC20Token...")
        erc20_token = deploy_contract(erc20_abi, erc20_bytecode, "Test ERC20", "T20", initial_supply_erc20, deployer)
        
        print("\n  Deploying MyERC721Token...")
        erc721_token = deploy_contract(erc721_abi, erc721_bytecode, "Test ERC721", "T721", deployer)
        
        print("\n  Deploying MockOracle...")
        mock_oracle = deploy_contract(oracle_abi, oracle_bytecode)
        
        print("\n  Deploying RWAManager...")
        rwa_manager = deploy_contract(rwa_manager_abi, rwa_manager_bytecode, erc20_token.address, deployer)
        
        print("\n  Deploying SimpleDAO...")
        simple_dao = deploy_contract(dao_abi, dao_bytecode, erc20_token.address, deployer)
        
        print("\nAll contracts deployed.")

    except Exception as e:
        print(f"\n!! Experiment initialization (load or deploy contracts) failed: {e}")
        print("Experiment cannot continue. Check error messages and Ganache logs.")
        return

    l1_gas_price_from_ganache_wei = w3.eth.gas_price # Get Ganache's current gas price (wei)
    l1_current_gas_price_gwei = float(w3.from_wei(l1_gas_price_from_ganache_wei, 'gwei'))
    print(f"Current L1 (Ganache) Gas Price: {l1_current_gas_price_gwei:.2f} Gwei (used for L2 cost simulation)")

    if not all([erc20_token, erc721_token, rwa_manager, simple_dao, mock_oracle]):
        print("!! Some core contracts were not deployed successfully. Cannot proceed with transaction tests.")
        return

    transactions_to_test = [
        {
            "name": "RWA Token Issuance (ERC-721)",
            "l1_action_func": lambda: erc721_token.functions.mint(user1, int(time.time())),
            "l1_account": deployer
        },
        {
            "name": "RWA Token Transfer (ERC-20)",
            "setup_l1_func": lambda: execute_l1_transaction(erc20_token.functions.transfer(user1, 100 * (10**18)), deployer),
            "l1_action_func": lambda: erc20_token.functions.transfer(user2, 50 * (10**18)),
            "l1_account": user1
        },
        {
            "name": "Yield Distribution (N=3 Holders)",
            "setup_l1_func": lambda: (
                execute_l1_transaction(erc20_token.functions.approve(rwa_manager.address, 1000 * (10**18)), deployer),
                execute_l1_transaction(rwa_manager.functions.depositRewardTokens(1000 * (10**18)), deployer, value_eth=0),
                # Ensure enough accounts for N=3 or adjust N based on available accounts
                [execute_l1_transaction(erc20_token.functions.transfer(w3.eth.accounts[i+3 if i+3 < len(w3.eth.accounts) else i], 1 * (10**12)), deployer) for i in range(min(3, len(w3.eth.accounts)-3))]
            ),
            "l1_action_func": lambda: rwa_manager.functions.distributeRewards([w3.eth.accounts[i+3 if i+3 < len(w3.eth.accounts) else i] for i in range(min(3, len(w3.eth.accounts)-3))]),
            "l1_account": deployer
        },
        {
            "name": "Governance Vote",
            "setup_l1_func": lambda: execute_l1_transaction(simple_dao.functions.createProposal("Test Proposal To Vote On"), deployer),
            "l1_action_func": lambda: simple_dao.functions.vote(0, True), # Vote on proposalId 0
            "l1_account": user1
        },
        {
            "name": "Oracle Update (Valuation)",
            "l1_action_func": lambda: mock_oracle.functions.updateAssetValue(12345, 50000 + int(time.time()%100)),
            "l1_account": deployer,
            "oracle_cost_usd": MOCK_ORACLE_SERVICE_FEE_USD
        }
    ]

    for tx_info in transactions_to_test:
        print(f"\n--- Testing Transaction Type: {tx_info['name']} ---")
        l1_total_gas_used = 0
        l1_total_cost_eth = 0
        l1_total_cost_usd = 0
        l1_successful_runs = 0
        l1_equivalent_gas_for_l2_calc_sum = 0

        # L1 Setup (if needed)
        if "setup_l1_func" in tx_info and tx_info["setup_l1_func"]:
            print("  Executing L1 setup...")
            setup_action_result = tx_info["setup_l1_func"]()
            # Check for single or multiple setup action failures
            if isinstance(setup_action_result, tuple) and setup_action_result[0] is None and setup_action_result[3] is not None and setup_action_result[3].status == 0:
                print(f"    L1 setup for '{tx_info['name']}' failed (reverted). Skipping L1 runs.")
                continue
            elif isinstance(setup_action_result, list):
                 if any(res is None or (isinstance(res, tuple) and res[0] is None and res[3] is not None and res[3].status == 0) for res in setup_action_result if res is not None):
                    print(f"    L1 setup for '{tx_info['name']}' had partial failures (reverted). Skipping L1 runs.")
                    continue
            print("    L1 setup complete.")

        # L1 Transaction Execution
        print("  Executing L1 transactions...")
        for i in range(num_runs_per_tx_type):
            # Call lambda here to get the contract function call object
            action_to_call = tx_info["l1_action_func"]()
            if action_to_call is None: # e.g. if a contract was not deployed
                 print(f"    L1 run {i+1} for '{tx_info['name']}' could not build transaction call (contract might be None).")
                 break # Break inner loop

            gas_used, cost_eth, cost_usd, receipt = execute_l1_transaction(action_to_call, tx_info["l1_account"])
            if gas_used is not None and receipt and receipt.status == 1:
                l1_total_gas_used += gas_used
                l1_total_cost_eth += cost_eth
                l1_total_cost_usd += cost_usd
                l1_equivalent_gas_for_l2_calc_sum += gas_used # Use actual gas used for L2 base
                l1_successful_runs += 1
            else:
                print(f"    L1 run {i+1} for '{tx_info['name']}' failed or reverted.")
            time.sleep(0.05) # Small delay between txs

        if l1_successful_runs > 0:
            avg_l1_gas_used = l1_total_gas_used / l1_successful_runs
            avg_l1_cost_eth = l1_total_cost_eth / l1_successful_runs
            avg_l1_cost_usd = l1_total_cost_usd / l1_successful_runs
            oracle_cost_l1 = tx_info.get("oracle_cost_usd", 0)

            results.append({
                "Transaction Type": tx_info['name'],
                "Platform": "Layer-1",
                "Avg. Gas Used": f"{avg_l1_gas_used:.0f}",
                "Avg. Tx Cost (ETH)": f"{avg_l1_cost_eth:.8f}",
                "Avg. Tx Cost (USD)": f"{avg_l1_cost_usd:.4f}",
                "Oracle Cost (USD)": f"{oracle_cost_l1:.4f}" if oracle_cost_l1 > 0 else "N/A",
                "Notes": f"L1 GasPrice: {float(w3.from_wei(w3.eth.gas_price, 'gwei')):.2f} Gwei" # Current Gas Price
            })
            print(f"    L1 Avg Gas: {avg_l1_gas_used:.0f}, Cost ETH: {avg_l1_cost_eth:.8f}, Cost USD: {avg_l1_cost_usd:.4f}")

            l1_avg_gas_for_l2_base = l1_equivalent_gas_for_l2_calc_sum / l1_successful_runs
            for batch_size in l2_batch_sizes_to_test:
                print(f"    Simulating L2 transaction (Batch Size: {batch_size})...")
                l2_gas_sim, l2_cost_eth, l2_cost_usd = calculate_l2_tx_cost(
                    l1_avg_gas_for_l2_base,
                    batch_size,
                    l1_current_gas_price_gwei # Use Ganache's current gas price for L2 sim
                )
                oracle_cost_l2 = tx_info.get("oracle_cost_usd", 0) # Oracle cost is platform-agnostic here
                results.append({
                    "Transaction Type": tx_info['name'],
                    "Platform": "Layer-2 (Simulated)",
                    "Avg. Gas Used": f"{l2_gas_sim:.0f} (L2 OpGas)", # This is the simulated L2 operational gas
                    "Avg. Tx Cost (ETH)": f"{l2_cost_eth:.8f}",
                    "Avg. Tx Cost (USD)": f"{l2_cost_usd:.4f}",
                    "Oracle Cost (USD)": f"{oracle_cost_l2:.4f}" if oracle_cost_l2 > 0 else "N/A",
                    "Notes": f"BS={batch_size}"
                })
                print(f"      L2 (BS={batch_size}) Simulated L2 OpGas: {l2_gas_sim:.0f}, Cost ETH: {l2_cost_eth:.8f}, Cost USD: {l2_cost_usd:.4f}")
        else:
            print(f"    L1 transactions for '{tx_info['name']}' all failed. Skipping cost recording for this type.")


    if results:
        df = pd.DataFrame(results)
        print("\n\n--- Cost Comparison Table (Simulated Results) ---")
        # Set pandas display options to avoid scientific notation and show more decimal places
        pd.set_option('display.float_format', lambda x: '%.8f' % x if isinstance(x, float) else x)
        print(df.to_string(max_colwidth=100)) # Print full table to console
        try:
            df.to_csv("rwa_cost_comparison_simulated.csv", index=False)
            print("\nResults saved to rwa_cost_comparison_simulated.csv")
        except Exception as e:
            print(f"\nFailed to save CSV file: {e}")
    else:
        print("\nNo successful transactions to analyze. Cost comparison table not generated.")

if __name__ == "__main__":
    run_experiment()