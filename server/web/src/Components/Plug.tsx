import React from 'react'
import yt from '../assets/youtube.png'
import github from '../assets/github.png'

const Plug = () => {
  return (
    <div>
        <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
         <a
           className="flex items-center gap-2 hover:underline hover:underline-offset-4 decoration-wavy text-red-100 text-xl animate-pulse hover:animate-none"
           href="https://www.youtube.com/@OAilouros"
           target="_blank"
           rel="noopener noreferrer"
         >
           <img
             aria-hidden
             src={yt}
             alt="youtube tutorial"
             width={32}
             height={32}
           />
           Idea
         </a>
         <a
           className="flex items-center gap-2 hover:underline hover:underline-offset-4 decoration-dotted text-red-100 text-xl animate-pulse hover:animate-none"
           href="https://github.com/ailourito/kawadonis"
           target="_blank"
           rel="noopener noreferrer"
         >
           <img
             aria-hidden
             src={github}
             alt="GitHub link"
             width={32}
             height={32}
           />
           Code
         </a>
       </footer>
    </div>
  )
}

export default Plug