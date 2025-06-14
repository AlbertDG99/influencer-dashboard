import torch

def check_gpu():
    """
    Checks for CUDA availability and prints GPU details.
    """
    print("--- GPU Sanity Check ---")
    
    if not torch.cuda.is_available():
        print("❌ CUDA is not available. The container cannot access the GPU.")
        print("Please ensure you have installed the NVIDIA Container Toolkit and that Docker is configured correctly.")
        return

    print("✅ CUDA is available!")
    
    device_count = torch.cuda.device_count()
    print(f"Found {device_count} GPU(s).")
    
    for i in range(device_count):
        gpu = torch.cuda.get_device_properties(i)
        print(f"\n--- GPU {i} ---")
        print(f"Name:          {gpu.name}")
        print(f"CUDA Version:  {torch.version.cuda}")
        
        total_memory_gb = gpu.total_memory / (1024**3)
        
        # Note: torch.cuda.mem_get_info() is more accurate for free memory
        free_memory_gb, _ = torch.cuda.mem_get_info(i)
        free_memory_gb /= (1024**3)
        
        print(f"Total VRAM:    {total_memory_gb:.2f} GB")
        print(f"Free VRAM:     {free_memory_gb:.2f} GB")
        print("--------------------")

if __name__ == "__main__":
    check_gpu() 