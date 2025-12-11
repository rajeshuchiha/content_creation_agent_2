export default function Loader() {
  return (
    <div className="flex items-center justify-center space-x-2">
      <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
      <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
      <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
    </div>
  );
}
// export default function Loader() {
//     return (
//         <div class="mx-auto w-full max-w-xl rounded-md border border-blue-300 p-4">
//             <div class="flex animate-pulse space-x-4">
//                 {/* <div class="size-10 rounded-full bg-gray-200"></div> */}
//                 <div class="flex-1 space-y-6 py-1">
//                     <div class="h-2 rounded bg-gray-200"></div>
//                     <div class="space-y-3">
//                         <div class="grid grid-cols-3 gap-4">
//                             <div class="col-span-2 h-2 rounded bg-gray-200"></div>
//                             <div class="col-span-1 h-2 rounded bg-gray-200"></div>
//                         </div>
//                         <div class="h-2 rounded bg-gray-200"></div>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// }