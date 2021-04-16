# Run: bash create_env.sh

# Create env
conda init
conda env create --name computer_vision -f environment.yml
conda activate computer_vision


# Save env
# conda env export > environment.yml

# Remove env
# conda remove -n [env_name] --all -y
