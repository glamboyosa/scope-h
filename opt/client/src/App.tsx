import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
type Tbgfetch = {
  task_id: number;
  status: boolean;
};
function App() {
  const push = useNavigate();
  const triggerProcess = useMutation<Tbgfetch>(
    (): Promise<Tbgfetch> =>
      fetch("http://localhost:8000/background-task/", { method: "POST" }).then(
        (res) => res.json()
      ),
    {
      onSuccess(data) {
        push(`/influencers?id=${data.task_id}`);
      },
      onError(error) {
        console.log(error);
      },
    }
  );

  return (
    <main className="flex justify-center items-center">
      <button
        onClick={() => triggerProcess.mutate()}
        className="p-4 rounded-md bg-pink-400 font-md hover:bg-pink-300"
      >
        Create Report 👩🏿‍🎤
      </button>
    </main>
  );
}

export default App;
